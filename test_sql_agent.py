import asyncio
from app.agent.graph import sql_agent_graph

async def main():
    print("Testing sql_agent_graph...")
    initial_state = {
        "question": "i want to apply leave today?",
        "user_id": "3153f599-3b1a-4cb8-b4bb-5cf2ee4fb79f",
        "role": "EMPLOYEE"
    }
    config = {"configurable": {"thread_id": "test_id"}}
    
    try:
        async for event in sql_agent_graph.astream(initial_state, config):
            print("EVENT:", event)
    except Exception as e:
        print("ERROR:", e)

if __name__ == "__main__":
    asyncio.run(main())
