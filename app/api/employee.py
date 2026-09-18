import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.common.deps import get_authenticated_user, get_hr_user
from app.services.employee_service import EmployeeService
from app.schema.employee_schema import (
    EmployeeResponse,
    UpdateEmployeeRequest,
    ListEmployeeResponse,
)

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/", response_model=ListEmployeeResponse)
async def list_employees(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await EmployeeService(db).get_all()


@router.get("/managers", response_model=ListEmployeeResponse)
async def list_managers(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await EmployeeService(db).get_managers()


@router.get("/me", response_model=EmployeeResponse)
async def get_me(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await EmployeeService(db).get_by_id(current_user.id)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(
    employee_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_authenticated_user),
):
    return await EmployeeService(db).get_by_id(employee_id)


@router.patch("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: uuid.UUID,
    request: UpdateEmployeeRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await EmployeeService(db).update(employee_id, request)


@router.delete("/{employee_id}", status_code=status.HTTP_200_OK)
async def delete_employee(
    employee_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_hr_user),
):
    return await EmployeeService(db).delete(employee_id)
