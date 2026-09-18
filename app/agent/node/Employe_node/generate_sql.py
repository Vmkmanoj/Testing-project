import logging
from app.agent.llm import get_llm
from app.agent.state import SQLAgentState
from app.database.database import Sql_agent

logger = logging.getLogger(__name__)


def generate(state: SQLAgentState):
    print("--- ENTERING NODE: generate_sql ---")
    llm = get_llm()
    retries = state.get("retries", 0) + 1

    error_msg = (
        f"\nPrevious error: {state.get('error')}\n" if state.get("error") else ""
    )

    prompt = f"""
    You are an expert PostgreSQL developer.

    Database Schema:

    {state['schema']}

    User Question:

    {state['question']}
    
    Current Context:
    - User ID: {state.get('user_id', 'Unknown')}
    - User Role: {state.get('role', 'Unknown')}
    - Current Date: CURRENT_DATE in PostgreSQL

    {error_msg}
    Generate only a SQL query.

    - Use PostgreSQL syntax.
    - Only generate SELECT, INSERT INTO leave_requests, OR UPDATE leave_requests queries.
    - Never generate DELETE, DROP, or ALTER.
    - If inserting a leave request:
        - `user_id` must be the Context User ID.
        - Look up `leave_type_id` dynamically (e.g., `(SELECT id FROM leave_types WHERE name ILIKE '%casual%')`).
        - If the user applies for leave on a weekend (Saturday or Sunday) or a government holiday, do NOT generate an INSERT query. Instead, generate exactly this query: SELECT 'it govmernt hollyday or it weekend it already leave date can you check the date' AS result;
        - If the user tries to apply for leave on a date they have already applied for (or if you see a database error indicating this), do NOT generate an INSERT query. Instead, generate exactly this query: SELECT 'you already applied on that date' AS result;
        - Look up `holiydate` dynamically (e.g., `(SELECT id FROM leave_types WHERE name ILIKE '%casual%')`).
        - Calculate `total_days` appropriately based on the dates.
        - You cannot apply for leave for a past date. Please select today or a future date.
        - Do not allow the user to apply for leave if the without date is not provided.
        -Generate the `id` using `gen_random_uuid()`.
        - You MUST end your INSERT statement with `RETURNING *;` so the database returns the inserted row.
    - If cancelling a leave request:
        - Use `UPDATE leave_requests SET status = 'CANCELLED'`.
        - Always filter by `user_id = '<Context User ID>'` and `status = 'PENDING'`.
        - If the user wants to cancel ALL requests, do not filter by date.
        - If the user provides a specific date, filter using `start_date = '<that date>'`.
        - You MUST end your UPDATE statement with `RETURNING *;` so the database returns the updated row(s).
    - If Reject a leave request:
        - Use `UPDATE leave_requests SET status = 'REJECTED'`.
        - This is ONLY allowed if the Context User Role is 'MANAGER' or 'HR'.
        - If the user wants to reject ALL pending requests, filter by `status = 'PENDING'`. (Do NOT filter by `user_id` unless they specify a particular user).
        - If the user provides a specific date, filter using `start_date = '<that date>'`.
        - You MUST end your UPDATE statement with `RETURNING *;` so the database returns the updated row(s).
    - If approving a leave request:
        - Use `UPDATE leave_requests SET status = 'APPROVED'`.
        - This is ONLY allowed if the Context User Role is 'MANAGER' or 'HR'.
        - If the user wants to approve ALL pending requests, filter by `status = 'PENDING'`. (Do NOT filter by `user_id` unless they specify a particular user).
        - If the user provides a specific date, filter using `start_date = '<that date>'`.
        - You MUST end your UPDATE statement with `RETURNING *;` so the database returns the updated row(s).
    - Return only SQL without markdown formatting or code blocks.
    - If the user asks about "my" data (e.g. "my leave balance", "my manager"), filter by their User ID using the context provided.
    - If the user asks a conversational question that doesn't need a DB query, just output a generic SELECT 1 query and the format node will handle the rest.
    - An employee can view only their own leave requests, leave history, leave balance, and leave details.
        HR and Managers can view leave details of employees they are authorized to manage.
        If an employee asks about another employee's leave details, the agent/backend should not provide any information and should respond:
        "You don't have permission to view that employee's leave details."
        Enforce this restriction in the backend using RBAC and authorization checks, not only in the UI.
        The UI should also hide or disable access to other employees' leave details for regular employees.
        Ensure the LangGraph agent/tools also respect these permissions and cannot expose leave information through another query or tool.
    """

    result = llm.invoke(prompt)

    sql_raw = result.content.strip()
    if sql_raw.startswith("```sql"):
        sql_raw = sql_raw[6:]
    if sql_raw.startswith("```"):
        sql_raw = sql_raw[3:]
    if sql_raw.endswith("```"):
        sql_raw = sql_raw[:-3]

    return {"sql_query": sql_raw.strip(), "retries": retries}
