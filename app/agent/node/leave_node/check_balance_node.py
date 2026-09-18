from app.agent.state import AgentState
from app.agent.tools.leave_tool import extract_employee_name, LeaveTool

async def run(state: AgentState) -> AgentState:
    user_message = state["user_message"]
    user_id = state.get("user_id")

    try:
        # Check if the user specified a name in their message
        target_name = await extract_employee_name(user_message)
        
        # Get the balance
        response_text = await LeaveTool.check_balance_tool(target_name, user_id)
        
        state["final_response"] = response_text
    except Exception as e:
        state["final_response"] = f"Failed to check leave balance: {e}"

    return state
