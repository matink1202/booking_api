from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID as postuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Service(Base):
    """_summary_

    Args:
        Base (_type_): provider_id: uuid, name: str, duration_minutes: int, price: decimal
    """
    
    __tablename__ = "services"
    
    id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("providers.id"), index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    
    provider: Mapped["Provider"] =relationship(back_populates="services")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="service")