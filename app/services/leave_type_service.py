import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_type_model import LeaveType
from app.repositories.leave_type_repository import LeaveTypeRepository
from app.schema.leave_type_schema import (
    CreateLeaveTypeRequest,
    UpdateLeaveTypeRequest,
    LeaveTypeResponse,
)


class LeaveTypeService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LeaveTypeRepository(db)

    def _to_response(self, lt: LeaveType) -> LeaveTypeResponse:
        return LeaveTypeResponse(
            id=str(lt.id),
            name=lt.name,
            description=lt.description,
            max_days_per_year=lt.max_days_per_year,
            is_active=lt.is_active,
        )

    async def create(self, request: CreateLeaveTypeRequest) -> LeaveTypeResponse:
        existing = await self.repo.get_by_name(request.name)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Leave type already exists.")
        lt = LeaveType(
            name=request.name,
            description=request.description,
            max_days_per_year=request.max_days_per_year,
        )
        lt = await self.repo.create(lt)
        await self.db.commit()
        return self._to_response(lt)

    async def get_all(self) -> list[LeaveTypeResponse]:
        return [self._to_response(lt) for lt in await self.repo.get_all()]

    async def get_by_id(self, leave_type_id: uuid.UUID) -> LeaveTypeResponse:
        lt = await self.repo.get_by_id(leave_type_id)
        if not lt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found.")
        return self._to_response(lt)

    async def update(self, leave_type_id: uuid.UUID, request: UpdateLeaveTypeRequest) -> LeaveTypeResponse:
        lt = await self.repo.get_by_id(leave_type_id)
        if not lt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found.")
        if request.name is not None:
            lt.name = request.name
        if request.description is not None:
            lt.description = request.description
        if request.max_days_per_year is not None:
            lt.max_days_per_year = request.max_days_per_year
        if request.is_active is not None:
            lt.is_active = request.is_active
        lt = await self.repo.update(lt)
        await self.db.commit()
        return self._to_response(lt)

    async def delete(self, leave_type_id: uuid.UUID) -> dict:
        lt = await self.repo.get_by_id(leave_type_id)
        if not lt:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave type not found.")
        await self.repo.delete(lt)
        await self.db.commit()
        return {"success": True, "message": "Leave type deleted."}
