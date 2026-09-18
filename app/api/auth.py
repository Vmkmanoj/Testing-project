from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.services.auth_service import AuthService
from app.schema.auth_schema import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
):
    service = AuthService(db)
    return await service.login(request)


from app.common.deps import get_hr_user

@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    hr_user = Depends(get_hr_user),
):
    service = AuthService(db)
    return await service.register(request)
