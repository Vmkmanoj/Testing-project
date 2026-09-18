import logging
from app.database.database import Sql_agent

logger = logging.getLogger(__name__)

def execute_sql(state):
    print("--- ENTERING NODE: execute_sql ---")

    try:

        result = Sql_agent.run(
            state["sql_query"]
        )

        return {
            "query_result": result
        }   

    except Exception as e:

        return {
            "error": str(e),
            "query_result": None
        }