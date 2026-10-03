from datetime import datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.appointment import Appointment as AppointmentModel
from app.models.appointment import AppointmentStatus
from app.models.provider import Provider as ProviderModel
from app.models.service import Service as ServiceModel
from app.models.user import UserRole


async def _has_conflict(
    db: AsyncSession,
    provider_id,
    start_time: datetime,
    end_time: datetime,
    exclude_appointment_id=None,
) -> bool:
    query = select(AppointmentModel).where(
        and_(
            AppointmentModel.provider_id == provider_id,
            AppointmentModel.status != AppointmentStatus.CANCELLED,
            AppointmentModel.start_time < end_time,
            AppointmentModel.end_time > start_time,
        )
    )
    if exclude_appointment_id is not None:
        query = query.where(AppointmentModel.id != exclude_appointment_id)

    result = await db.execute(query)
    return result.scalars().first() is not None


async def create_appointment(db, current_user, data) -> AppointmentModel:

    query = select(ServiceModel).where(ServiceModel.id == data.service_id)
    result = await db.execute(query)
    service = result.scalar_one_or_none()

    if service == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="appointment not exists"
        )

    end_time = data.start_time + timedelta(minutes=service.duration_minutes)

    if data.provider_id != service.provider_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this service don't blong to this provider",
        )

    if await _has_conflict(db, data.provider_id, data.start_time, end_time):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="this time slot is not available",
        )

    appointment_obj = AppointmentModel(
        customer_id=current_user.id,
        provider_id=service.provider_id,
        service_id=service.id,
        start_time=data.start_time,
        end_time=end_time,
        status=AppointmentStatus.PENDING,
    )

    db.add(appointment_obj)
    await db.commit()
    await db.refresh(appointment_obj)
    return appointment_obj


async def list_appointments(db, current_user, skip, limit) -> list[AppointmentModel]:

    if current_user.role == UserRole.CUSTOMER:
        query = (
            select(AppointmentModel)
            .where(AppointmentModel.customer_id == current_user.id)
            .order_by(AppointmentModel.id)
            .limit(limit)
            .offset(skip)
        )
    elif current_user.role == UserRole.PROVIDER:
        query = (
            select(AppointmentModel)
            .join(ProviderModel, AppointmentModel.provider_id == ProviderModel.id)
            .where(ProviderModel.user_id == current_user.id)
            .order_by(AppointmentModel.id)
            .limit(limit)
            .offset(skip)
        )
    else:
        query = (
            select(AppointmentModel)
            .order_by(ProviderModel.id)
            .limit(limit)
            .offset(skip)
        )

    result = await db.execute(query)
    appointments = result.scalars().all()

    return appointments


async def get_appointment(db, current_user, appointment_id) -> AppointmentModel:
    query = (
        select(AppointmentModel)
        .options(selectinload(AppointmentModel.provider))
        .where(AppointmentModel.id == appointment_id)
    )
    result = await db.execute(query)
    appointment = result.scalar_one_or_none()

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found"
        )

    is_owner = (
        appointment.customer_id == current_user.id
        or appointment.provider.user_id == current_user.id
    )
    if not (is_owner or current_user.role == UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have access to this appointment",
        )

    return appointment


async def update_appointment_status(
    db, current_user, appointment_id, data
) -> AppointmentModel:

    query = (
        select(AppointmentModel)
        .options(selectinload(AppointmentModel.provider))
        .where(AppointmentModel.id == appointment_id)
    )
    result = await db.execute(query)
    appointment = result.scalar_one_or_none()

    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="appointment not found",
        )

    is_owner_provider = appointment.provider.user_id == current_user.id

    if not (current_user.role == UserRole.ADMIN or is_owner_provider):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you don't have access to this appointment",
        )

    if data.status == AppointmentStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="use the cancel endpoint to cancel an appointment",
        )

    appointment.status = data.status
    await db.commit()
    await db.refresh(appointment)
    return appointment


async def cancel_appointment(
    db, current_user, appointment_id, data
) -> AppointmentModel:

    query = (
        select(AppointmentModel)
        .options(selectinload(AppointmentModel.provider))
        .where(AppointmentModel.id == appointment_id)
    )
    result = await db.execute(query)
    appointment = result.scalar_one_or_none()

    if appointment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="appointment not found")

    is_owner = (
        appointment.customer_id == current_user.id
        or appointment.provider.user_id == current_user.id
    )
    if not (is_owner or current_user.role == UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="you don't have access to this appointment"
        )

    appointment.status = AppointmentStatus.CANCELLED
    await db.commit()
    await db.refresh(appointment)
    return appointment
