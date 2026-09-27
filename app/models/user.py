from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy import Enum as enum
from sqlalchemy.dialects.postgresql import UUID as postuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    PROVIDER = "provider"
    CUSTOMER = "customer"


class User(Base):
    """_summary_

    Args:
        Base (_type_): full_name: str, email: str, hashed_password: str
    """
    
    __tablename__ = "users"

    id: Mapped[UUID] =mapped_column(
            postuuid(as_uuid=True), primary_key=True, default=uuid4
        )
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        enum(UserRole), default=UserRole.CUSTOMER, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    provider_profile: Mapped["Provider"] = relationship(back_populates="user", uselist=False)
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="customer")