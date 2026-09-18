import logging
from app.agent.state import SQLAgentState

logger = logging.getLogger(__name__)


def validate_sql(state: SQLAgentState):
    print("--- ENTERING NODE: validate_sql ---")

    sql = state["sql_query"].strip().upper()

    dangerous_keywords = ["DELETE", "DROP", "ALTER", "TRUNCATE"]

    print("retries number", state.get("retries"))

    for keyword in dangerous_keywords:
        if keyword in sql:
            return {
                "validation_result": "invalid",
                "error": f"Dangerous SQL detected: {keyword}",
            }

    if "UPDATE" in sql:
        # Only allow updating leave_requests
        if not ("UPDATE LEAVE_REQUESTS" in sql or 'UPDATE "leave_requests"' in sql):
            return {
                "validation_result": "invalid",
                "error": "Only UPDATE on leave_requests is allowed",
            }

        is_cancelled = "SET STATUS" in sql and "'CANCELLED'" in sql
        is_approved = "SET STATUS" in sql and "'APPROVED'" in sql

        if not (is_cancelled or is_approved):
            return {
                "validation_result": "invalid",
                "error": "Only UPDATE leave_requests SET status = 'CANCELLED' or 'APPROVED' is allowed",
            }

        if is_approved:
            user_role = state.get("role", "").upper()
            if user_role not in ["MANAGER", "HR"]:
                return {
                    "validation_result": "invalid",
                    "error": "Only MANAGER or HR can approve leave requests.",
                }

    # Check INSERT logic
    elif "INSERT" in sql:
        # Only allow insert into leave_requests
        if not (
            "INSERT INTO LEAVE_REQUESTS" in sql or 'INSERT INTO "leave_requests"' in sql
        ):
            return {
                "validation_result": "invalid",
                "error": "Only INSERT into leave_requests is allowed",
            }
    elif not sql.startswith("SELECT"):
        return {
            "validation_result": "invalid",
            "error": "Only SELECT, INSERT INTO leave_requests, or UPDATE leave_requests queries are allowed",
        }

    print("sql queru", state["sql_query"])

    if "INSERT" in sql or "UPDATE" in sql:
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
            confirmation_message = "Are you sure you want to proceed with this modification? \n\nPlease reply with 'yes' to confirm or 'no' to cancel."

        return {
            "validation_result": "needs_confirmation",
            "awaiting_confirmation": True,
            "final_answer": confirmation_message
        }

    return {"validation_result": "valid"}
