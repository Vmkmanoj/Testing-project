from app.agent.state import AgentState
from app.agent.tools.leave_tool import LeaveTool



async def run(state : AgentState) -> AgentState:

    details_list = state.get("extracted_data", [])

    print("tool_input", details_list)

    if not isinstance(details_list, list):
        details_list = [details_list]

    results = []
    messages = []
    
    for idx, details in enumerate(details_list, 1):
        try:
            result = await LeaveTool.create_leave(
                state["user_id"],
                details["start_date"],
                details["end_date"],
                details["leave_type"],
                details["reason"]
            )
            results.append(result)
            messages.append(f"Request {idx} (from {details['start_date']} to {details['end_date']}): {result['message']}")
        except Exception as e:
            results.append(None)
            messages.append(f"Request {idx} (from {details.get('start_date')} to {details.get('end_date')}): Failed - {str(e)}")

    state["tool_result"] = {"results": results}
    state["pending_action"] = None
    
    if all(r is not None for r in results):
        state["final_response"] = "All leave requests were created successfully!\n\n" + "\n".join(messages)
    elif any(r is not None for r in results):
        state["final_response"] = "Some leave requests were created, but others failed:\n\n" + "\n".join(messages)
    else:
        state["final_response"] = "Failed to create leave requests:\n\n" + "\n".join(messages)
    
    return state




