from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password, verify_password
from app.models.user import User as UserModel
from app.schemas.user import UserCreateSchema


async def register_user(db: AsyncSession, data: UserCreateSchema) -> UserModel:
    
    query = select(UserModel).where(UserModel.email == data.email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already registered")
    
    user_hash_password = hash_password(data.password)
    user_obj = UserModel(full_name=data.full_name, email= data.email, hashed_password= user_hash_password)
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    
    return user_obj


async def authenticate_user(db: AsyncSession, email: str, password: str) -> UserModel:
    query = select(UserModel).where(UserModel.email == email)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user and verify_password(password, user.hashed_password):
        return user
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="incorrect email or password")
    