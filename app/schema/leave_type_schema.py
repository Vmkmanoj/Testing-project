from pydantic import BaseModel


class CreateLeaveTypeRequest(BaseModel):
    name: str
    description: str | None = None
    max_days_per_year: int


class UpdateLeaveTypeRequest(BaseModel):
    name: str | None = None
    description: str | None = None
    max_days_per_year: int | None = None
    is_active: bool | None = None


class LeaveTypeResponse(BaseModel):
    id: str
    name: str
    description: str | None = None
    max_days_per_year: int
    is_active: bool

    class Config:
        from_attributes = True
