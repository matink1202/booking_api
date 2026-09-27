from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str = Field(description="user token")
    token_type: str = Field(default="bearer", description="user token typre")
