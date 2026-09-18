import logging
from app.database.database import Sql_agent

logger = logging.getLogger(__name__)

def get_schema(state):
    print("--- ENTERING NODE: get_schema ---")

    schema = Sql_agent.get_table_info()

    return {
        "schema": schema
    }