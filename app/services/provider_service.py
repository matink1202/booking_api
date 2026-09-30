from fastapi import HTTPException, status
from sqlalchemy import select

from app.models.provider import Provider as ProviderModel
from app.models.user import UserRole


async def create_provider_profile(db, current_user, data) -> ProviderModel:

    query = select(ProviderModel).where(ProviderModel.user_id == current_user.id)
    result = await db.execute(query)
    provider = result.scalar_one_or_none()

    if provider:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="provider already exists"
        )

    provider_obj = ProviderModel(
        user_id=current_user.id, bio=data.bio, specialty=data.specialty
    )
    db.add(provider_obj)

    if current_user.role == UserRole.CUSTOMER:
        current_user.role = UserRole.PROVIDER
        db.add(current_user)

    await db.commit()
    await db.refresh(provider_obj)

    return provider_obj


async def get_provider(db, provider_id) -> ProviderModel:

    query = select(ProviderModel).where(ProviderModel.id == provider_id)
    result = await db.execute(query)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="provider not exists"
        )

    return provider


async def list_providers(db, skip: int, limit: int) -> list[ProviderModel]:

    query = select(ProviderModel).order_by(ProviderModel.id).limit(limit).offset(skip)
    result = await db.execute(query)
    provider = result.scalars().all()

    return provider


async def update_provider(db, current_user, provider_id, data) -> ProviderModel:

    query = select(ProviderModel).where(ProviderModel.id == provider_id)
    result = await db.execute(query)
    provider = result.scalar_one_or_none()

    if not provider:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="provider not exists"
        )

    if current_user.role == UserRole.ADMIN or provider.user_id == current_user.id:
        provider_update = data.model_dump(exclude_unset=True)

        for key, value in provider_update.items():
            setattr(provider, key, value)

        await db.commit()
        await db.refresh(provider)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have access to this provider",
        )

    return provider
