import uuid
from datetime import date

from sqlalchemy import (
    String,
    Date,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True
    )

    start_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="PLANNING"
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False
    )

    client = relationship(
        "Client",
        back_populates="projects"
    )

    teams = relationship(
        "Team",
        back_populates="project",
        cascade="all, delete-orphan"
    )