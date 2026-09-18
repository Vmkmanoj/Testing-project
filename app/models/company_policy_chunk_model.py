from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.company_policy_model import CompanyPolicy


class CompanyPolicyChunk(Base):
    __tablename__ = "company_policy_chunks"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid4
    )

    policy_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("company_policies.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    embedding: Mapped[list[float]] = mapped_column(Vector(384), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    policy: Mapped["CompanyPolicy"] = relationship(
        "CompanyPolicy", back_populates="chunks"
    )

    __table_args__ = (
        UniqueConstraint("policy_id", "chunk_index", name="uq_policy_chunk"),
    )
