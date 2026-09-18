
from app.agent.state import AgentState
from app.agent.tools.leave_tool import LeaveTool , extract_leave_details


async def run(state : AgentState) -> AgentState:

    details_list = await extract_leave_details(state["user_message"])

    print("details : ", details_list)

    if not details_list:
        state["final_response"] = "I couldn't understand your leave request. Could you please provide the dates?"
        return state

    for details in details_list:
        if not details.get("start_date") or not details.get("end_date"):
            state["final_response"] = (
                 "I'd like to help you apply for leave — could you tell me the start "
                "and end dates (e.g. 2026-10-02 to 2026-10-04) and the leave type "
                "(casual, sick, or earned)?"
            )
            return state

    try: 
        state["extracted_data"] = details_list
        state["pending_action"] = "CREATE_LEAVE_REQUEST"
        state["awaiting_confirmation"] = True
        state["confirmed"] = None

        response_lines = ["Please verify your leave request(s):", ""]
        for i, details in enumerate(details_list, 1):
            response_lines.append(f"Request {i}:")
            response_lines.append(f"📅 Start Date: {details.get('start_date')}")
            response_lines.append(f"📅 End Date: {details.get('end_date')}")
            response_lines.append(f"🏥 Leave Type: {details.get('leave_type')}")
            response_lines.append(f"📝 Reason: {details.get('reason') or 'Not provided'}")
            response_lines.append("")

        response_lines.append("Do you want to submit these leave requests? (Yes/No)")

        state["final_response"] = "\n".join(response_lines)

    except Exception as e:
        state["final_response"] = f"Failed to parse leave requests: {e}"

    return state

    
        
        
