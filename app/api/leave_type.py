import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.common.deps import get_hr_user, get_authenticated_user
from app.services.leave_type_service import LeaveTypeService
from app.schema.leave_type_schema import (
    CreateLeaveTypeRequest,
    UpdateLeaveTypeRequest,
    LeaveTypeResponse,
)

router = APIRouter(prefix="/leave-types", tags=["Leave Types"])


@router.post("/", response_model=LeaveTypeResponse, status_code=status.HTTP_201_CREATED)
async def create_leave_type(
    request: CreateLeaveTypeRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveTypeService(db).create(request)


@router.get("/", response_model=list[LeaveTypeResponse])
async def list_leave_types(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await LeaveTypeService(db).get_all()


@router.get("/{leave_type_id}", response_model=LeaveTypeResponse)
async def get_leave_type(
    leave_type_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveTypeService(db).get_by_id(leave_type_id)


@router.patch("/{leave_type_id}", response_model=LeaveTypeResponse)
async def update_leave_type(
    leave_type_id: uuid.UUID,
    request: UpdateLeaveTypeRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveTypeService(db).update(leave_type_id, request)


@router.delete("/{leave_type_id}", status_code=status.HTTP_200_OK)
async def delete_leave_type(
    leave_type_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await LeaveTypeService(db).delete(leave_type_id)
