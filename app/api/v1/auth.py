from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.token import TokenSchema
from app.schemas.user import UserCreateSchema, UserLoginSchema, UserOutSchema
from app.services import auth_service

router = APIRouter(tags=["auth"], prefix="/auth")


@router.post("/register", response_model=UserOutSchema, status_code=status.HTTP_201_CREATED)
async def user_register(request: UserCreateSchema, db: AsyncSession = Depends(get_db)):  # noqa: B008
    user = await auth_service.register_user(db, request)
    return user


@router.post("/login", response_model=TokenSchema)
async def user_login(request: UserLoginSchema, db: AsyncSession = Depends(get_db)):  # noqa: B008
    user = await auth_service.authenticate_user(db, request.email, request.password)
    token = create_access_token(str(user.id))
    return TokenSchema(access_token=token)