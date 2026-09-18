import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.common.deps import get_authenticated_user, get_hr_user, get_manager_user, get_hr_or_manager_user
from app.services.leave_request_service import LeaveRequestService
from app.schema.leave_request_schema import (
    CreateLeaveRequestRequest,
    ApproveLeaveRequest,
    LeaveRequestResponse,
    LeaveApprovalResponse,
    PaginatedLeaveRequests,
)

router = APIRouter(prefix="/leave-requests", tags=["Leave Requests"])


@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_request(
    request: CreateLeaveRequestRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await LeaveRequestService(db).create(current_user.id, request)


@router.get("/me", response_model=PaginatedLeaveRequests)
async def get_my_requests(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    skip = (page - 1) * limit
    return await LeaveRequestService(db).get_my_requests(current_user.id, skip, limit)


@router.get("/", response_model=PaginatedLeaveRequests)
async def get_all_requests(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_or_manager_user),
):
    skip = (page - 1) * limit
    return await LeaveRequestService(db).get_all(skip, limit)


@router.patch("/{request_id}/action", response_model=LeaveApprovalResponse)
async def approve_or_reject(
    request_id: uuid.UUID,
    request: ApproveLeaveRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_or_manager_user),
):
    return await LeaveRequestService(db).approve_or_reject(
        request_id, current_user.id, request
    )
