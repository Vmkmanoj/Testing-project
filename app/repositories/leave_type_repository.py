import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_type_model import LeaveType


class LeaveTypeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, leave_type: LeaveType) -> LeaveType:
        self.db.add(leave_type)
        await self.db.flush()
        return leave_type

    async def get_all(self) -> list[LeaveType]:
        result = await self.db.execute(select(LeaveType))
        return result.scalars().all()

    async def get_by_id(self, leave_type_id: uuid.UUID) -> LeaveType | None:
        result = await self.db.execute(
            select(LeaveType).where(LeaveType.id == leave_type_id)
        )
        return result.scalars().first()

    async def get_by_name(self, name: str) -> LeaveType | None:
        result = await self.db.execute(
            select(LeaveType).where(LeaveType.name == name)
        )
        return result.scalars().first()

    async def update(self, leave_type: LeaveType) -> LeaveType:
        self.db.add(leave_type)
        await self.db.flush()
        return leave_type

    async def delete(self, leave_type: LeaveType) -> None:
        await self.db.delete(leave_type)
        await self.db.flush()
