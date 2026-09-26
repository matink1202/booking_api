from uuid import UUID, uuid4

from app.db.base import Base
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as postuuid
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Provider(Base):
    __tablename__ = "providers"
    
    id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(postuuid(as_uuid=True), ForeignKey("users.id"), unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(Text, nullable=True)
    specialty: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    user: Mapped["User"] = relationship(back_populates="provider_profile")
    services: Mapped[list["Service"]] = relationship(back_populates="provider")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="provider")