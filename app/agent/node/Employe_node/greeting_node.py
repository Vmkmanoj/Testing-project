from app.agent.state import SQLAgentState
from app.agent.llm import get_llm


async def greeting(state: SQLAgentState):
    print("--- ENTERING NODE: greeting ---")

    prompt = """
    You are a friendly Employee Management Assistant.

    The user has sent a greeting or simple casual message.

    Respond briefly, warmly, and professionally.
    Ask how you can help with employee or leave management.

    Do not:
    - Make up employee information
    - Apply leave
    - Query the database
    - Give policy information unless the user asks for it

    Examples:

    User: "Hi"
    Assistant: "Hi! How can I help you today?"

    User: "Hello"
    Assistant: "Hello! How can I help you with your employee or leave management?"

    User: "Good morning"
    Assistant: "Good morning! How can I help you today?"
    """

    question = state.get("question", "")

    messages = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": question
        }
    ]

    response = await get_llm().ainvoke(messages)

    return {
        "final_answer": response.content
    }