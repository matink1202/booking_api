from decimal import Decimal

from pydantic import UUID4, BaseModel, ConfigDict, Field


class ServiceCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="service name")
    duration_minutes: int = Field(..., gt=0, description="how long is the service")
    price: Decimal = Field(..., ge=0, max_digits=10, decimal_places=2)


class ServiceUpdateSchema(BaseModel):
    name: str | None = Field(
        default=None, min_length=2, max_length=100, description="service name"
    )
    duration_minutes: int | None = Field(
        default=None, gt=0, description="how long is the service"
    )
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)


class ServiceOutSchema(BaseModel):
    id: UUID4 = Field(description="service id")
    provider_id: UUID4 = Field(description="provider's id that provide")
    name: str = Field(min_length=2, max_length=100, description="service name")
    duration_minutes: int = Field(gt=0, description="how long is the service")
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)

    model_config = ConfigDict(from_attributes=True)
