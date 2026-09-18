from pydantic import BaseModel
from uuid import UUID
from datetime import date


class CreateLeaveRequestRequest(BaseModel):
    leave_type_id: UUID
    start_date: date
    end_date: date
    total_days: int
    reason: str | None = None


class ApproveLeaveRequest(BaseModel):
    action: str  # "APPROVED" or "REJECTED"
    comment: str | None = None


class LeaveRequestResponse(BaseModel):
    id: str
    user_id: str
    leave_type_id: str
    start_date: date
    end_date: date
    total_days: int
    reason: str | None = None
    status: str

    class Config:
        from_attributes = True


class LeaveApprovalResponse(BaseModel):
    id: str
    leave_request_id: str
    approved_by: str
    action: str
    comment: str | None = None

    class Config:
        from_attributes = True


class PaginatedLeaveRequests(BaseModel):
    items: list[LeaveRequestResponse]
    total: int
    page: int
    limit: int
