from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.common.deps import get_hr_user, get_db

from app.services.create_employee_service import CreateEmployeeService
from app.schema.client_schema import CreateClientRequest


router = APIRouter(prefix="/client", tags=["Client"])



@router.post("/create")
async def create_client(
    request : CreateClientRequest,
    current_user = Depends(get_hr_user), db: AsyncSession = Depends(get_db)
):
    service = CreateEmployeeService(db)
    return await service.create_client(request)



    