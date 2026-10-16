from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.availability import (
    ProviderAvailability as ProviderAvailabilityModel,
)
from app.models.provider import Provider as ProviderModel
from app.models.user import UserRole


async def create_availability(db, current_user, data) -> ProviderAvailabilityModel:
    query = select(ProviderModel).where(ProviderModel.user_id == current_user.id)
    result = await db.execute(query)
    provider = result.scalar_one_or_none()

    if provider is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="provider profile missing"
        )

    availability_obj = ProviderAvailabilityModel(
        provider_id=provider.id,
        day_of_week=data.day_of_week,
        start_time=data.start_time,
        end_time=data.end_time,
    )

    db.add(availability_obj)
    await db.commit()
    await db.refresh(availability_obj)

    return availability_obj


async def list_availability(
    db, provider_id, skip, limit
) -> list[ProviderAvailabilityModel]:
    query = (
        select(ProviderAvailabilityModel)
        .where(ProviderAvailabilityModel.provider_id == provider_id)
        .order_by(ProviderAvailabilityModel.day_of_week)
        .limit(limit)
        .offset(skip)
    )
    result = await db.execute(query)
    return result.scalars().all()


async def delete_availability(db, current_user, availability_id) -> None:
    query = (
        select(ProviderAvailabilityModel)
        .options(selectinload(ProviderAvailabilityModel.provider))
        .where(ProviderAvailabilityModel.id == availability_id)
    )
    result = await db.execute(query)
    availability = result.scalar_one_or_none()

    if availability is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="this availability doesn't exist",
        )

    is_owner = availability.provider.user_id == current_user.id
    if not (is_owner or current_user.role == UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have access to this availability",
        )

    await db.delete(availability)
    await db.commit()
