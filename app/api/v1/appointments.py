from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.appointment import (
    AppointmentCreateSchema,
    AppointmentOutSchema,
    AppointmentRescheduleSchema,
    AppointmentStatusUpdateSchema,
)
from app.services import booking_services

router = APIRouter(tags=["appointments"], prefix="/appointments")


@router.post(
    "/", response_model=AppointmentOutSchema, status_code=status.HTTP_201_CREATED
)
async def create_appointment(
    request: AppointmentCreateSchema,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):

    appointment = await booking_services.create_appointment(db, current_user, request)
    return appointment


@router.get(
    "/", response_model=list[AppointmentOutSchema], status_code=status.HTTP_200_OK
)
async def get_appointments(
    limit: int = Query(
        20, gt=0, le=100, description="limiting the number of items to retrieve"
    ),
    skip: int = Query(0, ge=0, description="use for paginating based on passed items"),
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):

    appointments = await booking_services.list_appointments(
        db, current_user, skip, limit
    )
    return appointments


@router.get(
    "/{appointment_id}",
    response_model=AppointmentOutSchema,
    status_code=status.HTTP_200_OK,
)
async def get_appointment_detail(
    appointment_id: UUID = Path(..., description="appointment id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):

    appointment = await booking_services.get_appointment(
        db, current_user, appointment_id
    )
    return appointment


@router.patch(
    "/{appointment_id}",
    response_model=AppointmentOutSchema,
    status_code=status.HTTP_200_OK,
)
async def update_appointment(
    request: AppointmentStatusUpdateSchema,
    appointment_id: UUID = Path(..., description="appointment id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    appointment = await booking_services.update_appointment_status(
        db, current_user, appointment_id, request
    )
    return appointment


@router.patch("/{appointment_id}/reschedule", response_model=AppointmentOutSchema)
async def reschedule_appointment(
    request: AppointmentRescheduleSchema,
    appointment_id: UUID = Path(..., description="appointment id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    return await booking_services.reschedule_appointment(
        db, current_user, appointment_id, request
    )


@router.post(
    "/{appointment_id}/cancel",
    response_model=AppointmentOutSchema,
    status_code=status.HTTP_200_OK,
)
async def cancel_appointment(
    appointment_id: UUID = Path(..., description="appointment id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    return await booking_services.cancel_appointment(db, current_user, appointment_id)
