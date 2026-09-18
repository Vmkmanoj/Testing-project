from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User
from app.models.role_model import Role
from app.models.user_role_model import UserRole
from app.common.enums import RoleName

from sqlalchemy.orm import selectinload

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        stmt = select(User).options(selectinload(User.roles)).where(User.email == email)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_user(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_role_by_name(self, role_name: RoleName | str) -> Role | None:
        if isinstance(role_name, RoleName):
            role_name = role_name.value
        stmt = select(Role).where(Role.name == role_name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def assign_role_to_user(self, user_id, role_id) -> UserRole:
        user_role = UserRole(user_id=user_id, role_id=role_id)
        self.db.add(user_role)
        await self.db.flush()
        return user_role
