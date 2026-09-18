from sqlalchemy import false
from app.agent.state import SQLAgentState


async def confirmation(state: SQLAgentState) -> dict:

    message = state["question"].strip().lower()

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
        "do it",
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
        "don't do it",
    ]

    if message in yes_word:

        state["confirmed"] = True
        state["awaiting_confirmation"] = False

        return state

    if message in no_word:

        state["confirmed"] = False
        state["awaiting_confirmation"] = False

        state["pending_action"] = None
        state["final_answer"] = "Your request has been cancelled."

        return state

    state["final_answer"] = (
        "Please reply with Yes to submit " "or No to cancel your leave request."
    )

    return state
