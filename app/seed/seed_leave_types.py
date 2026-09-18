from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_type_model import LeaveType


LEAVE_TYPES = [
    {
        "name": "SICK_LEAVE",
        "description": "Leave for medical reasons",
        "max_days_per_year": 10
    },
    {
        "name": "CASUAL_LEAVE",
        "description": "Leave for personal reasons",
        "max_days_per_year": 12
    },
    {
        "name": "ANNUAL_LEAVE",
        "description": "Paid annual vacation leave",
        "max_days_per_year": 15
    },
    {
        "name": "UNPAID_LEAVE",
        "description": "Leave without salary",
        "max_days_per_year": 365
    }
]


async def seed_leave_types(db: AsyncSession):

    for leave_data in LEAVE_TYPES:

        result = await db.execute(
            select(LeaveType).where(
                LeaveType.name == leave_data["name"]
            )
        )

        leave_type = result.scalar_one_or_none()

        if not leave_type:

            leave_type = LeaveType(
                name=leave_data["name"],
                description=leave_data["description"],
                max_days_per_year=leave_data["max_days_per_year"]
            )

            db.add(leave_type)

    await db.commit()

    print("Leave types seeded successfully!")