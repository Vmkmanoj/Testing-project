from sqlalchemy import select, or_, func
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.user_model import User


class EmployeeRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[User]:
        result = await self.db.execute(
            select(User).options(selectinload(User.roles), selectinload(User.manager))
        )
        return result.scalars().all()

    async def get_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(
            select(User).options(selectinload(User.roles), selectinload(User.manager)).where(User.id == user_id)
        )
        return result.scalars().first()

    async def update(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.flush()

    async def get_user_by_name(self, name: str):

        name = name.strip()
        full_name = func.concat(
            User.first_name,
            " ",
            User.last_name
        )

        stmt = select(User).where(
            or_(
                User.first_name.ilike(f"%{name}%"),
                User.last_name.ilike(f"%{name}%"),
                full_name.ilike(f"%{name}%")
            )
        )

        result = await self.db.execute(stmt)

        user = result.scalars().first()

        if not user:
            return None

        return {
            "id": str(user.id),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}"
        }
