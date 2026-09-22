import logging
import re
from app.agent.state import SQLAgentState

logger = logging.getLogger(__name__)

# Personal / sensitive tables — employees should only see their own rows
_PERSONAL_TABLES = [
    "employees",
    "leave_requests",
    "leave_balances",
    "salaries",
    "attendance",
    "leave_history",
]


def _is_unauthorized_employee_query(sql: str, user_id: str) -> bool:
    """
    Returns True if an EMPLOYEE role generated SQL that could expose another
    employee's personal data.

    Rules:
    1. If the query is an ACCESS DENIED sentinel → not unauthorized (allow it
       to flow through so format_answer shows the message).
    2. If the query touches a personal table but does NOT filter by the
       requester's own user_id / employee_id → block it.
    3. If the query explicitly references a DIFFERENT user_id in a WHERE
       clause → block it.
    """
    sql_upper = sql.upper()
    sql_lower = sql.lower()

    # Rule 0: Let the ACCESS DENIED sentinel pass — it is already the safe response
    if "ACCESS DENIED" in sql_upper:
        return False

    # Rule 0b: Generic no-op queries are fine
    if sql_upper.strip() in ("SELECT 1", "SELECT 1;"):
        return False

    # Check whether the query touches any personal table
    touches_personal = any(t in sql_lower for t in _PERSONAL_TABLES)

    if not touches_personal:
        # Not touching sensitive tables — allow (e.g. SELECT from leave_types)
        return False

    # Rule 1: Query must contain the requester's own user_id as a literal filter.
    # Accept formats like:
    #   WHERE user_id = 'abc-123'
    #   WHERE employee_id = 'abc-123'
    #   user_id = '{user_id}'  (in case LLM outputs placeholder)
    uid_lower = str(user_id).lower()
    has_own_filter = (
        uid_lower in sql_lower
        or f"user_id = '{uid_lower}'" in sql_lower
        or f"employee_id = '{uid_lower}'" in sql_lower
    )

    if not has_own_filter:
        # Query touches a personal table but doesn't filter by the requester's ID
        logger.warning(
            "RBAC: EMPLOYEE query touches personal table without own user_id filter. Blocking."
        )
        return True

    # Rule 2: If ANY other UUID-like string appears explicitly in the SQL
    # (suggesting the LLM injected a different user's ID), block it.
    uuid_pattern = re.compile(
        r"['\"]([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})['\"]",
        re.IGNORECASE,
    )
    found_ids = uuid_pattern.findall(sql)
    for found_id in found_ids:
        if found_id.lower() != uid_lower:
            logger.warning(
                f"RBAC: EMPLOYEE query contains a different user UUID ({found_id}). Blocking."
            )
            return True

    return False


def validate_sql(state: SQLAgentState):
    print("--- ENTERING NODE: validate_sql ---")

    sql = state["sql_query"].strip()
    sql_upper = sql.upper()

    user_role = state.get("role", "").upper()
    user_id = state.get("user_id", "")

    print("retries number", state.get("retries"))

    # ==========================================================
    # HARD RBAC CHECK (runs BEFORE any other validation)
    # If the LLM generated an unauthorized cross-user query for
    # an EMPLOYEE, block it immediately — no execution allowed.
    # ==========================================================
    if user_role == "EMPLOYEE":
        if _is_unauthorized_employee_query(sql, user_id):
            logger.warning(
                f"RBAC BLOCK: employee {user_id} generated unauthorized SQL: {sql[:120]}"
            )
            return {
                "validation_result": "unauthorized",
                "final_answer": (
                    "🚫 **Access Denied**\n\n"
                    "You do not have permission to view another employee's personal data, "
                    "leave details, or salary information.\n\n"
                    "Only **HR** and **Managers** can access other employees' information. "
                    "You can only view your own data."
                ),
            }

    # ==========================================================
    # DANGEROUS KEYWORD CHECK
    # ==========================================================
    dangerous_keywords = ["DELETE", "DROP", "ALTER", "TRUNCATE"]
    for keyword in dangerous_keywords:
        if keyword in sql_upper:
            return {
                "validation_result": "invalid",
                "error": f"Dangerous SQL detected: {keyword}",
            }

    # ==========================================================
    # UPDATE validation
    # ==========================================================
    if "UPDATE" in sql_upper:
        # Only allow updating leave_requests
        if not ("UPDATE LEAVE_REQUESTS" in sql_upper or 'UPDATE "leave_requests"' in sql_upper):
            return {
                "validation_result": "invalid",
                "error": "Only UPDATE on leave_requests is allowed",
            }

        is_cancelled = "SET STATUS" in sql_upper and "'CANCELLED'" in sql_upper
        is_approved  = "SET STATUS" in sql_upper and "'APPROVED'"  in sql_upper
        is_rejected  = "SET STATUS" in sql_upper and "'REJECTED'"  in sql_upper

        if not (is_cancelled or is_approved or is_rejected):
            return {
                "validation_result": "invalid",
                "error": "Only UPDATE leave_requests SET status = 'CANCELLED', 'APPROVED', or 'REJECTED' is allowed",
            }

        # Only MANAGER / HR can approve or reject
        if is_approved or is_rejected:
            if user_role not in ["MANAGER", "HR"]:
                return {
                    "validation_result": "unauthorized",
                    "final_answer": (
                        "🚫 **Access Denied**\n\n"
                        "Only **HR** and **Managers** can approve or reject leave requests."
                    ),
                }

    # ==========================================================
    # INSERT validation
    # ==========================================================
    elif "INSERT" in sql_upper:
        if not (
            "INSERT INTO LEAVE_REQUESTS" in sql_upper
            or 'INSERT INTO "leave_requests"' in sql_upper
        ):
            return {
                "validation_result": "invalid",
                "error": "Only INSERT into leave_requests is allowed",
            }

    elif not sql_upper.startswith("SELECT"):
        return {
            "validation_result": "invalid",
            "error": "Only SELECT, INSERT INTO leave_requests, or UPDATE leave_requests queries are allowed",
        }

    print("sql query", state["sql_query"])

    # ==========================================================
    # CONFIRMATION REQUIRED for write operations
    # ==========================================================
    if "INSERT" in sql_upper or "UPDATE" in sql_upper:
        from app.agent.llm import get_llm
        llm = get_llm()
        if llm:
            prompt = f"""
            The user wants to make a change to their data. 
            User's original request: "{state.get('question')}"
            The generated SQL query for this change is:
            {sql}
            
            Write a short, natural, and friendly confirmation message asking the user if they want to proceed with this specific change. 
            Extract the key details (like dates, leave type, action) from the SQL/request and include them in the message.
            Do NOT show the raw SQL. 
            End the message by asking them to reply with 'yes' to confirm or 'no' to cancel.
            """
            response = llm.invoke(prompt)
            confirmation_message = response.content
        else:
            confirmation_message = (
                "Are you sure you want to proceed with this modification?\n\n"
                "Please reply with 'yes' to confirm or 'no' to cancel."
            )

        return {
            "validation_result": "needs_confirmation",
            "awaiting_confirmation": True,
            "final_answer": confirmation_message,
        }

    return {"validation_result": "valid"}
