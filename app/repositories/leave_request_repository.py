import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.leave_request_model import LeaveRequest
from app.models.leave_approval_model import LeaveApproval


class LeaveRequestRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        await self.db.flush()
        return leave_request

    async def count_by_user(self, user_id: uuid.UUID) -> int:
        result = await self.db.execute(
            select(func.count(LeaveRequest.id)).where(LeaveRequest.user_id == user_id)
        )
        return result.scalar()

    async def get_by_user(self, user_id: uuid.UUID, skip: int = 0, limit: int = 10) -> list[LeaveRequest]:
        result = await self.db.execute(
            select(LeaveRequest)
            .where(LeaveRequest.user_id == user_id)
            .order_by(LeaveRequest.start_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def count_all(self) -> int:
        result = await self.db.execute(select(func.count(LeaveRequest.id)))
        return result.scalar()

    async def get_all(self, skip: int = 0, limit: int = 10) -> list[LeaveRequest]:
        result = await self.db.execute(
            select(LeaveRequest)
            .order_by(LeaveRequest.start_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, request_id: uuid.UUID) -> LeaveRequest | None:
        result = await self.db.execute(
            select(LeaveRequest).where(LeaveRequest.id == request_id)
        )
        return result.scalars().first()

    async def add_approval(self, approval: LeaveApproval) -> LeaveApproval:
        self.db.add(approval)
        await self.db.flush()
        return approval

    async def update(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        await self.db.flush()
        return leave_request

    async def get_pending_by_user(self, user_id: uuid.UUID) -> LeaveRequest | None:
        result = await self.db.execute(
            select(LeaveRequest).where(LeaveRequest.user_id == user_id).where(LeaveRequest.status == "PENDING")
        )
        return result.scalars().first()

    async def delete(self, leave_request: LeaveRequest):
        await self.db.delete(leave_request)
        
            


