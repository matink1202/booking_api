from pydantic import UUID4, BaseModel, ConfigDict, Field


class ProviderCreateSchema(BaseModel):
    bio: str | None = Field(default=None, description="a short text about provider")
    specialty: str | None = Field(
        default=None, max_length=100, description="what are they provide"
    )


class ProviderUpdateSchema(ProviderCreateSchema):
    model_config = ConfigDict(from_attributes=True)


class ProviderOutSchema(ProviderCreateSchema):
    id: UUID4 = Field(description="provider id")
    user_id: UUID4 = Field(description="user's id that book")

    model_config = ConfigDict(from_attributes=True)
