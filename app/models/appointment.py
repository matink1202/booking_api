from datetime import datetime
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy import Enum as enum
from sqlalchemy.dialects.postgresql import UUID as postuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Appointment(Base):
    """_summary_

    Args:
        Base (_type_): customer_id: uuid, provider_id:uuid, service_id: uuid, start_time: datatime, end_time: datetime, status: appointmentstatus
    """    
    
    __tablename__ = "appointments"
    
    id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), primary_key=True, default=uuid4)
    customer_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    provider_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("providers.id"), nullable=False, index=True)
    service_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("services.id"), nullable=False, index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[Enum] = mapped_column(enum(AppointmentStatus), default=AppointmentStatus.PENDING, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    customer: Mapped["User"] = relationship(back_populates="appointments")
    provider: Mapped["Provider"] = relationship(back_populates="appointments")
    service: Mapped["Service"] = relationship(back_populates="appointments")