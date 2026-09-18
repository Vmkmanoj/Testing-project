import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LeaveApproval(Base):
    __tablename__ = "leave_approvals"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    leave_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("leave_requests.id", ondelete="CASCADE"),
        nullable=False
    )

    approved_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(30),
        nullable=False
        # APPROVED / REJECTED
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    action_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    leave_request = relationship(
        "LeaveRequest",
        back_populates="approvals"
    )

    approver = relationship(
        "User"
    )