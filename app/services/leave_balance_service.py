import uuid
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_balance_model import LeaveBalance
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from app.repositories.leave_type_repository import LeaveTypeRepository
from app.schema.leave_balance_schema import (
    CreateLeaveBalanceRequest,
    UpdateLeaveBalanceRequest,
    LeaveBalanceResponse,
)


class LeaveBalanceService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LeaveBalanceRepository(db)
        self.leave_type_repo = LeaveTypeRepository(db)

    def _to_response(self, b: LeaveBalance) -> LeaveBalanceResponse:
        return LeaveBalanceResponse(
            id=str(b.id),
            user_id=str(b.user_id),
            leave_type_id=str(b.leave_type_id),
            leave_type_name=b.leave_type.name if b.leave_type else None,
            year=b.year,
            total_days=b.total_days,
            used_days=b.used_days,
        )

    async def create_for_user(self, request: CreateLeaveBalanceRequest) -> LeaveBalanceResponse:
        existing = await self.repo.get_by_user_and_type(
            request.user_id, request.leave_type_id, request.year
        )
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Leave balance already exists for this user, type, and year.")
        balance = LeaveBalance(
            user_id=request.user_id,
            leave_type_id=request.leave_type_id,
            year=request.year,
            total_days=request.total_days,
            used_days=0,
        )
        balance = await self.repo.create(balance)
        await self.db.commit()
        return self._to_response(balance)

    async def auto_create_for_user(self, user_id: uuid.UUID) -> list[LeaveBalanceResponse]:
        """Auto-create balances for all active leave types for the current year."""
        current_year = date.today().year
        leave_types = await self.leave_type_repo.get_all()
        created = []
        for lt in leave_types:
            if not lt.is_active:
                continue
            existing = await self.repo.get_by_user_and_type(user_id, lt.id, current_year)
            if not existing:
                balance = LeaveBalance(
                    user_id=user_id,
                    leave_type_id=lt.id,
                    year=current_year,
                    total_days=lt.max_days_per_year,
                    used_days=0,
                )
                balance = await self.repo.create(balance)
                created.append(self._to_response(balance))
        return created

    async def get_my_balance(self, user_id: uuid.UUID) -> list[LeaveBalanceResponse]:
        balances = await self.repo.get_by_user(user_id)
        return [self._to_response(b) for b in balances]

    async def update(
        self, user_id: uuid.UUID, leave_type_id: uuid.UUID, year: int, request: UpdateLeaveBalanceRequest
    ) -> LeaveBalanceResponse:
        balance = await self.repo.get_by_user_and_type(user_id, leave_type_id, year)
        if not balance:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave balance not found.")
        if request.total_days is not None:
            balance.total_days = request.total_days
        if request.used_days is not None:
            balance.used_days = request.used_days
        balance = await self.repo.update(balance)
        await self.db.commit()
        return self._to_response(balance)
