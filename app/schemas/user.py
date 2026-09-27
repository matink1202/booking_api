from pydantic import UUID4, BaseModel, EmailStr, Field

from app.models.user import UserRole


class UserCreateSchema(BaseModel):
    email: EmailStr = Field(..., description="user email")
    password: str = Field(..., min_length=8, description="user password")
    full_name: str = Field(..., min_length=2, description="user full name")


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., description="email of user")
    password: str = Field(..., description="user password")


class UserOutSchema(BaseModel):
    id: UUID4 = Field(description="user id")
    email: EmailStr = Field(description="email of user")
    full_name: str = Field(description="user full name")
    role: UserRole = Field(description="user role")
