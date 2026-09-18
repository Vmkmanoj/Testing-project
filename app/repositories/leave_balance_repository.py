import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_balance_model import LeaveBalance


from sqlalchemy.orm import selectinload


class LeaveBalanceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, balance: LeaveBalance) -> LeaveBalance:
        self.db.add(balance)
        await self.db.flush()
        return balance

    async def get_by_user(self, user_id: uuid.UUID) -> list[LeaveBalance]:
        result = await self.db.execute(
            select(LeaveBalance)
            .options(selectinload(LeaveBalance.leave_type))
            .where(LeaveBalance.user_id == user_id)
        )
        return result.scalars().all()

    async def get_by_user_and_type(
        self, user_id: uuid.UUID, leave_type_id: uuid.UUID, year: int
    ) -> LeaveBalance | None:
        result = await self.db.execute(
            select(LeaveBalance).where(
                LeaveBalance.user_id == user_id,
                LeaveBalance.leave_type_id == leave_type_id,
                LeaveBalance.year == year,
            )
        )
        return result.scalars().first()

    async def update(self, balance: LeaveBalance) -> LeaveBalance:
        self.db.add(balance)
        await self.db.flush()
        return balance
