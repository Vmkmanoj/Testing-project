import asyncio
from app.api.agent import async_generator
from app.agent.graph import sql_agent_graph

async def main():
    print("Testing async_generator...")
    sql_initial_state = {"question": "how many users are there?"}
    config = {"configurable": {"thread_id": "test"}}
    try:
        async for item in async_generator(sql_agent_graph, sql_initial_state, config):
            print(item)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
