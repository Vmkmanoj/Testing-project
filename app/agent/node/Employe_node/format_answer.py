import logging
from app.agent.llm import get_llm

logger = logging.getLogger(__name__)
llm = get_llm()

def format_answer(state):
    print("--- ENTERING NODE: format_answer ---")

    prompt = f"""
User Question:

{state.get("question")}

SQL Query Generated:

{state.get("sql_query", "None")}

Database Result:

{state.get("query_result", "None")}

Error (if any):

{state.get("error", "None")}

Give a highly natural, conversational, and helpful answer to the user based on the database result.
If the database result contains multiple rows or columns, summarize the information in plain English sentences (e.g. "We have 2 clients: Apple and Microsoft") rather than dumping the raw data.
CRITICAL: Do NOT output markdown tables, raw database rows, or technical IDs. Present the data seamlessly in a conversational way.

If there was an error generating or running the query, or if the question is unrelated to the database, answer the user conversationally and gracefully (e.g. "I'm sorry, I don't have access to that information in the database right now.").

VERY IMPORTANT SCOPE RESTRICTION:
You are strictly an AI assistant for an Employee Management system. 
If the user asks a general knowledge question, coding question, or anything completely unrelated to employee management (e.g., "what is python", "write a poem", "what is the weather"), you MUST outright refuse to answer it. 
Instead, reply exactly or similarly to: "I am an AI assistant specifically for employee management. I cannot answer general knowledge questions." Do not answer the question under any circumstances.

Do not mention unnecessary technical details, SQL queries, or internal errors.
Speak directly to the user as a helpful AI assistant.
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content
    }