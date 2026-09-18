import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    leave_type_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leave_types.id"),
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    total_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    reason: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        CheckConstraint("status IN ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED')", name="chk_leave_request_status"),
        default="PENDING",
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="leave_requests"
    )

    leave_type = relationship(
        "LeaveType",
        back_populates="leave_requests"
    )

    approvals = relationship(
        "LeaveApproval",
        back_populates="leave_request",
        cascade="all, delete-orphan"
    )