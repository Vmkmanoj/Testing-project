from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.auth_schema import RegisterRequest, RegisterResponse
from app.services.auth_service import AuthService
from app.common.deps import get_hr_user, get_db



router = APIRouter(prefix="/create-employee", tags=["Create Employee"])

@router.post("/")
async def create_employee(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    hr_user = Depends(get_hr_user),
):
    service = AuthService(db)
    return await service.register(request)

