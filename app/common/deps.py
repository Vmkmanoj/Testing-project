from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt import verify_access_token
from app.database.database import get_db
from app.repositories.auth_repository import AuthRepository
from app.common.enums import RoleName

from sqlalchemy import select, func
from app.models.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    if not token:
        return None
    try:
        payload = verify_access_token(token)
    except Exception:
        return None

    email = payload.get("email")
    if email is None:
        return None

    repo = AuthRepository(db)
    return await repo.get_user_by_email(email)


async def get_authenticated_user(current_user=Depends(get_current_user)):
    """Require any logged-in user regardless of role."""
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return current_user


async def get_manager_user(
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    role_name = current_user.roles[0].name if current_user.roles else None
    if role_name != RoleName.MANAGER.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Manager can perform this action",
        )
    return current_user


async def get_hr_user(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(func.count(User.id)))
    count = result.scalar()
    if count == 0:
        return None  # Allow first user to register

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )

    role_name = current_user.roles[0].name if current_user.roles else None
    if role_name != RoleName.HR.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR can perform this action",
        )
    return current_user

async def get_hr_or_manager_user(
    current_user=Depends(get_current_user), db: AsyncSession = Depends(get_db)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    role_name = current_user.roles[0].name if current_user.roles else None
    if role_name not in [RoleName.HR.value, RoleName.MANAGER.value]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only HR or Manager can perform this action",
        )
    return current_user
