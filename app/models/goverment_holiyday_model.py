import uuid
from datetime import date, datetime

from sqlalchemy import String, Date, Boolean, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint
from app.database.base import Base


class GovernmentHoliday(Base):
    __tablename__ = "government_holidays"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    holiday_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    holiday_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    state: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


    __table_args__ = (
    UniqueConstraint(
        "holiday_date",
        "name",
        "state",
        name="uq_government_holiday"
    ),
)