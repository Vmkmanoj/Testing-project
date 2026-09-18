import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User

from app.repositories.employee_repository import EmployeeRepository
from app.schema.employee_schema import (
    EmployeeResponse,
    UpdateEmployeeRequest,
    ListEmployeeResponse,
)


class EmployeeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = EmployeeRepository(db)

    def _to_response(self, user: User) -> EmployeeResponse:
        role_name = user.roles[0].name if user.roles else "UNKNOWN"
        manager_id = str(user.manager_id) if user.manager_id else None
        manager_name = f"{user.manager.first_name} {user.manager.last_name or ''}".strip() if user.manager else None

        return EmployeeResponse(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            is_active=user.is_active,
            role=role_name,
            manager_id=manager_id,
            manager_name=manager_name,
        )

    async def get_all(self) -> ListEmployeeResponse:
        employees = await self.repo.get_all()
        return ListEmployeeResponse(
            success=True,
            total=len(employees),
            employees=[self._to_response(e) for e in employees],
        )

    async def get_managers(self) -> ListEmployeeResponse:
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from app.models.role_model import Role
        
        # Return only active employees with the MANAGER role
        stmt = (
            select(User)
            .join(User.roles)
            .where(User.is_active == True, Role.name == "MANAGER")
            .options(selectinload(User.roles), selectinload(User.manager))
        )
        result = await self.db.execute(stmt)
        employees = result.scalars().all()
        return ListEmployeeResponse(
            success=True,
            total=len(employees),
            employees=[self._to_response(e) for e in employees],
        )

    async def get_user_name(self,name) -> EmployeeResponse:
        user = await self.repo.get_user_by_name(name)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return user
    

    async def get_by_id(self, user_id: uuid.UUID) -> EmployeeResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        return self._to_response(user)

    async def update(self, user_id: uuid.UUID, request: UpdateEmployeeRequest) -> EmployeeResponse:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

        if request.first_name is not None:
            user.first_name = request.first_name
        if request.last_name is not None:
            user.last_name = request.last_name
        if request.is_active is not None:
            user.is_active = request.is_active
        if request.manager_id is not None:
            if request.manager_id == "":
                user.manager_id = None
            else:
                try:
                    manager_uuid = uuid.UUID(request.manager_id)
                    if manager_uuid == user.id:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Employee cannot be their own manager.")
                    manager = await self.db.get(User, manager_uuid)
                    if not manager:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Assigned manager does not exist.")
                    user.manager_id = manager_uuid
                except ValueError:
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid manager ID format.")

        user = await self.repo.update(user)
        await self.db.commit()
        return self._to_response(user)

    async def delete(self, user_id: uuid.UUID) -> dict:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
        await self.repo.delete(user)
        await self.db.commit()
        return {"success": True, "message": "Employee deleted successfully."}
