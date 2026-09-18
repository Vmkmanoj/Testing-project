from sqlalchemy import false
from app.agent.state import AgentState


async def run(state : AgentState) -> AgentState:


    message = state["user_message"].strip().lower()

    yes_word = [
        "yes",
        "confirm",
        "sure",
        "apply",
        "submit",
        "ok",
        "okay",
        "okey",
        "yep",
        "aye",
        "affirmative",
        "right",
        "correct",
        "proceed",
        "approve",
        "accept",
        "go ahead",
        "continue",
        "do it"
    ]

    no_word = [
        "no",
        "cancel",
        "not now",
        "later",
        "never",
        "stop",
        "nope",
        "nay",
        "negative",
        "wrong",
        "incorrect",
        "don't do it"
    ]

    if message in yes_word:

        state["confirmed"] = True
        state["awaiting_confirmation"] = False

        return state

    if message in no_word:

        state["confirmed"] = False
        state["awaiting_confirmation"] = False

        state["pending_action"] = None
        state["final_response"] = (
            "Yes leave request has been cancelled"
        )

        return state

    state["final_response"] = (
        "Please reply with Yes to submit "
        "or No to cancel your leave request."
    )

    return state


    