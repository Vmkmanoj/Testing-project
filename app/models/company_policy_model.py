from datetime import date, datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.company_policy_chunk_model import CompanyPolicyChunk

from sqlalchemy import Boolean, Date, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class CompanyPolicy(Base):
    __tablename__ = "company_policies"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    policy_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    file_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    file_url: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    version: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    effective_from: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    effective_until: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    chunks: Mapped[list["CompanyPolicyChunk"]] = relationship(
        "CompanyPolicyChunk",
        back_populates="policy",
        cascade="all, delete-orphan"
    )