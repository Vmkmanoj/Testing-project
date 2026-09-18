from app.agent.state import AgentState
from app.agent.tools.leave_tool import LeaveTool


async def run(state:AgentState) -> AgentState:
    userId = state.get("user_id")

    if not userId:
        state["final_response"] = "I couldn't find your user ID to cancel the leave."
        return state

    try:
        result = await LeaveTool.cancel_leave_tool(userId)
        state["tool_result"] = result
        state["final_response"] = result["message"]

    except Exception as e:
        state["final_response"] = f"Failed to cancel leave: {e}"

    return state
