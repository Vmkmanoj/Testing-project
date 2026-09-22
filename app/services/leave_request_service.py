import uuid
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.leave_request_model import LeaveRequest
from app.models.leave_approval_model import LeaveApproval
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.repositories.leave_balance_repository import LeaveBalanceRepository
from app.schema.leave_request_schema import (
    CreateLeaveRequestRequest,
    ApproveLeaveRequest,
    LeaveRequestResponse,
    LeaveApprovalResponse,
    PaginatedLeaveRequests,
)
from datetime import datetime

from app.services.mail_service import send_mail_information
from app.repositories.employee_repository import EmployeeRepository

class LeaveRequestService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = LeaveRequestRepository(db)
        self.balance_repo = LeaveBalanceRepository(db)
        self.employee_repo = EmployeeRepository(db)


    def _to_response(self, lr: LeaveRequest) -> LeaveRequestResponse:
        return LeaveRequestResponse(
            id=str(lr.id),
            user_id=str(lr.user_id),
            leave_type_id=str(lr.leave_type_id),
            start_date=lr.start_date,
            end_date=lr.end_date,
            total_days=lr.total_days,
            reason=lr.reason,
            status=lr.status,
        )

    async def create(
        self, user_id: uuid.UUID, request: CreateLeaveRequestRequest
    ) -> LeaveRequestResponse:
        # Validate dates
        if request.end_date < request.start_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="end_date cannot be before start_date.",
            )

        # Check balance
        year = request.start_date.year
        balance = await self.balance_repo.get_by_user_and_type(
            user_id, request.leave_type_id, year
        )
        if not balance:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No leave balance found for this leave type.",
            )
        remaining = balance.total_days - balance.used_days
        if request.total_days > remaining:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient leave balance. You have {remaining} days remaining.",
            )

        lr = LeaveRequest(
            user_id=user_id,
            leave_type_id=request.leave_type_id,
            start_date=request.start_date,
            end_date=request.end_date,
            total_days=request.total_days,
            reason=request.reason,
            status="PENDING",
        )
        lr = await self.repo.create(lr)
        await self.db.commit()
        return self._to_response(lr)

    async def get_my_requests(
        self, user_id: uuid.UUID, skip: int = 0, limit: int = 10
    ) -> PaginatedLeaveRequests:
        total = await self.repo.count_by_user(user_id)
        requests = await self.repo.get_by_user(user_id, skip, limit)
        items = [self._to_response(lr) for lr in requests]
        page = (skip // limit) + 1 if limit > 0 else 1
        return PaginatedLeaveRequests(items=items, total=total, page=page, limit=limit)

    async def get_all(self, skip: int = 0, limit: int = 10) -> PaginatedLeaveRequests:
        total = await self.repo.count_all()
        requests = await self.repo.get_all(skip, limit)
        items = [self._to_response(lr) for lr in requests]
        page = (skip // limit) + 1 if limit > 0 else 1
        return PaginatedLeaveRequests(items=items, total=total, page=page, limit=limit)

    async def approve_or_reject(
        self,
        request_id: uuid.UUID,
        approver_id: uuid.UUID,
        request: ApproveLeaveRequest,
    ) -> LeaveApprovalResponse:
        if request.action not in ("APPROVED", "REJECTED"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="action must be APPROVED or REJECTED.",
            )

        lr = await self.repo.get_by_id(request_id)
        if not lr:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found."
            )
        if lr.status != "PENDING":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Leave request is already {lr.status}.",
            )

        # Deduct balance on approval
        if request.action == "APPROVED":
            balance = await self.balance_repo.get_by_user_and_type(
                lr.user_id, lr.leave_type_id, lr.start_date.year
            )
            if balance:
                balance.used_days += lr.total_days
                await self.balance_repo.update(balance)

        lr.status = request.action

        await self.repo.update(lr)

        get_user = await self.employee_repo.get_by_id(lr.user_id)

        await send_mail_information(worker=get_user, subject="Leave Request", message="Leave Accepeted")

        approval = LeaveApproval(
            leave_request_id=lr.id,
            approved_by=approver_id,
            action=request.action,
            comment=request.comment,
            action_at=datetime.utcnow(),
        )
        approval = await self.repo.add_approval(approval)
        await self.db.commit()

        return LeaveApprovalResponse(
            id=str(approval.id),
            leave_request_id=str(approval.leave_request_id),
            approved_by=str(approval.approved_by),
            action=approval.action,
            comment=approval.comment,
        )

    async def cancel_pending_leave_request(self, user_id: uuid.UUID) -> dict:
        pending_request = await self.repo.get_pending_by_user(user_id)
        if not pending_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No pending leave request found for this user.",
            )

        await self.repo.delete(pending_request)

        get_user = await self.employee_repo.get_by_id(user_id)

        await send_mail_information(worker=get_user, subject="Leave Request", message="Leave Cancelled")

        await self.db.commit()
        return {
            "success": True,
            "message": "Your pending leave request has been cancelled successfully.",
        }
