from datetime import time
from uuid import UUID, uuid4

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Time
from sqlalchemy.dialects.postgresql import UUID as postuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ProviderAvailability(Base):
    """_summary_

    Args:
        Base (_type_): provider_id: uuid, day_of_week: int(0-6), start_time: time, end_time: time
    """    
    
    __tablename__ = "provider_availabilities"
    __table_args__ = (
        CheckConstraint("day_of_week >= 0 AND day_of_week <= 6", name="ck_day_of_week_range"),
    )
    
    id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("providers.id"), index=True)
    day_of_week: Mapped[int] = mapped_column(Integer)
    start_time: Mapped[time] = mapped_column(Time)
    end_time: Mapped[time] = mapped_column(Time)
    
    
    provider: Mapped["Provider"] = relationship(back_populates="availabilities")