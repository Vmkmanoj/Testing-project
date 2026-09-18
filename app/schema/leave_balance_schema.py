from pydantic import BaseModel
from uuid import UUID


class CreateLeaveBalanceRequest(BaseModel):
    user_id: UUID
    leave_type_id: UUID
    year: int
    total_days: int


class UpdateLeaveBalanceRequest(BaseModel):
    total_days: int | None = None
    used_days: int | None = None


class LeaveBalanceResponse(BaseModel):
    id: str
    user_id: str
    leave_type_id: str
    leave_type_name : str
    year: int
    total_days: int
    used_days: int

    class Config:
        from_attributes = True
