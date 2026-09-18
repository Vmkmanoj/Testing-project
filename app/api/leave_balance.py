import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.common.deps import get_authenticated_user, get_hr_user
from app.services.leave_balance_service import LeaveBalanceService
from app.schema.leave_balance_schema import (
    CreateLeaveBalanceRequest,
    UpdateLeaveBalanceRequest,
    LeaveBalanceResponse,
)

router = APIRouter(prefix="/leave-balances", tags=["Leave Balances"])


@router.post("/", response_model=LeaveBalanceResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_balance(
    request: CreateLeaveBalanceRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveBalanceService(db).create_for_user(request)


@router.get("/me", response_model=list[LeaveBalanceResponse])
async def get_my_balance(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await LeaveBalanceService(db).get_my_balance(current_user.id)


@router.patch("/{user_id}/{leave_type_id}/{year}", response_model=LeaveBalanceResponse)
async def update_leave_balance(
    user_id: uuid.UUID,
    leave_type_id: uuid.UUID,
    year: int,
    request: UpdateLeaveBalanceRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveBalanceService(db).update(user_id, leave_type_id, year, request)
