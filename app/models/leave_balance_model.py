import uuid

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class LeaveBalance(Base):
    __tablename__ = "leave_balances"

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
        ForeignKey("leave_types.id", ondelete="CASCADE"),
        nullable=False
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    total_days: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    used_days: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "leave_type_id",
            "year",
            name="uq_leave_balance_user_type_year"
        ),
    )

    user = relationship(
        "User",
        back_populates="leave_balances"
    )

    leave_type = relationship(
        "LeaveType",
        back_populates="leave_balances"
    )