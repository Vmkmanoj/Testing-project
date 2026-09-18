import asyncio
from app.database.database import AsyncSessionLocal
from app.services.employee_service import EmployeeService

async def main():
    async with AsyncSessionLocal() as db:
        try:
            res = await EmployeeService(db).get_managers()
            print("Success!", res.total)
        except Exception as e:
            print("Error:", e)

asyncio.run(main())
