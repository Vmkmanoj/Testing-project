# app/models/user.py

import uuid

from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)

    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)

    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )

    password: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    manager_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    manager = relationship("User", remote_side=[id], back_populates="subordinates")
    
    subordinates = relationship("User", back_populates="manager")

    roles = relationship("Role", secondary="user_roles", back_populates="users")

    teams = relationship("TeamMember", back_populates="user")

    leave_balances = relationship(
        "LeaveBalance", back_populates="user", cascade="all, delete-orphan"
    )

    leave_requests = relationship(
        "LeaveRequest", back_populates="user", cascade="all, delete-orphan"
    )
