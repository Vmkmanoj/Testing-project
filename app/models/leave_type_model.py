import uuid

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LeaveType(Base):
    __tablename__ = "leave_types"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    max_days_per_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    leave_balances = relationship(
        "LeaveBalance",
        back_populates="leave_type"
    )

    leave_requests = relationship(
        "LeaveRequest",
        back_populates="leave_type"
    )