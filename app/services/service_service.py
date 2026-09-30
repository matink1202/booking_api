from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.provider import Provider as ProviderModel
from app.models.service import Service as ServiceModel
from app.models.user import UserRole


async def create_service(db, current_user, data) -> ServiceModel:

    query = select(ProviderModel).where(ProviderModel.user_id == current_user.id)
    result = await db.execute(query)
    provider = result.scalar_one_or_none()

    if provider == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="create provider profile first",
        )

    service_obj = ServiceModel(
        provider_id=provider.id,
        name=data.name,
        duration_minutes=data.duration_minutes,
        price=data.price,
    )

    db.add(service_obj)
    await db.commit()
    await db.refresh(service_obj)

    return service_obj


async def list_services(
    db, skip: int, limit: int, provider_id: UUID | None
) -> list[ServiceModel]:

    query = select(ServiceModel).order_by(ServiceModel.id).limit(limit).offset(skip)

    if provider_id is not None:
        query = query.where(ServiceModel.provider_id == provider_id)

    result = await db.execute(query)
    service = result.scalars().all()

    return service


async def get_service(db, service_id) -> ServiceModel:

    query = select(ServiceModel).where(ServiceModel.id == service_id)
    result = await db.execute(query)
    service = result.scalar_one_or_none()

    if service == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="create service first"
        )

    return service


async def update_service(db, current_user, service_id, data) -> ServiceModel:

    query = (
        select(ServiceModel)
        .options(selectinload(ServiceModel.provider))
        .where(ServiceModel.id == service_id)
    )
    result = await db.execute(query)
    service = result.scalar_one_or_none()

    if service == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="create service first"
        )

    if (
        current_user.role == UserRole.ADMIN
        or service.provider.user_id == current_user.id
    ):
        service_update = data.model_dump(exclude_unset=True)

        for key, value in service_update.items():
            setattr(service, key, value)

        await db.commit()
        await db.refresh(service)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have access to this provider",
        )

    return service


async def delete_service(db, current_user, service_id) -> None:

    query = (
        select(ServiceModel)
        .options(selectinload(ServiceModel.provider))
        .where(ServiceModel.id == service_id)
    )
    result = await db.execute(query)
    service = result.scalar_one_or_none()

    if service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="service not found"
        )

    if (
        current_user.role == UserRole.ADMIN
        or service.provider.user_id == current_user.id
    ):
        await db.delete(service)
        await db.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you have not access to this service",
        )
