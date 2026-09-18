from pydantic import BaseModel
from uuid import UUID


class EmployeeResponse(BaseModel):
    id: str
    first_name: str
    last_name: str | None = None
    email: str
    is_active: bool
    role: str
    manager_id: str | None = None
    manager_name: str | None = None

    class Config:
        from_attributes = True


class UpdateEmployeeRequest(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool | None = None
    manager_id: str | None = None


class ListEmployeeResponse(BaseModel):
    success: bool
    total: int
    employees: list[EmployeeResponse]
