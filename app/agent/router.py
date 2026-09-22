from app.agent.llm import get_llm
from app.agent.state import AgentState  , SQLAgentState
from app.agent.prompts.system_prompts import INTENT_CLASSIFIER_PROMPT, CANCEL_REQUEST

VALID_INTENTS = {
    "apply_leave",
    "check_balance",
    "check_status",
    "cancel_leave",
    "reject_leave",
    "policy",
    "greeting",
    "database_query",
    "goverment_holiday"
}


def _llm_router_intent(message: str) -> str:
    llm = get_llm()
    if llm is not None:
        response = llm.invoke(INTENT_CLASSIFIER_PROMPT.format(message=message))
        label = response.content.strip().lower()
        return label if label in VALID_INTENTS else "greeting"
    return "greeting"


def router_intent(state: SQLAgentState ) -> str:

    if state.get("awaiting_confirmation"):
        return "confirmation"

    message = state.get("question", "")

    if get_llm() is not None:
        try:
            intent = _llm_router_intent(message)
            if intent == "greeting":
                return "greeting"
            elif intent == "policy":
                return "policy" 
            elif intent == "reject_leave":
                return "reject_leave"
            else:
                return "get_schema"
        except Exception as e:
            print(e)
            return "greeting"
    return "greeting"


def confirmation_router(state: SQLAgentState) -> str:
    if state.get("confirmed") is True:
        return "execute_sql"

    return "format_answer"


def check_validation(state : SQLAgentState):

    if state.get("validation_result") == "valid":
        return "execute_sql"

    # Unauthorized access attempt — final_answer already set, show it directly
    if state.get("validation_result") == "unauthorized":
        return "format_answer"
        
    if state.get("validation_result") == "needs_confirmation":
        return "end"

    if state.get("retries", 0) >= 3:
        
        return "format_answer"

    if state.get("greeting_responce") == "greeting":
        return "greeting"


    return "generate_sql"
