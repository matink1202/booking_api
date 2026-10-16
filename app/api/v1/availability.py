from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User as UserModel
from app.models.user import UserRole
from app.schemas.availability import AvailabilityCreateSchema, AvailabilityOutSchema
from app.services import availability_service

router = APIRouter(tags=["Availabilities"], prefix="/availabilities")


@router.post(
    "/", response_model=AvailabilityOutSchema, status_code=status.HTTP_201_CREATED
)
async def create_availability(
    request: AvailabilityCreateSchema,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(require_roles(UserRole.ADMIN, UserRole.PROVIDER)),  # noqa: B008
):
    availability = await availability_service.create_availability(
        db, current_user, request
    )
    return availability


@router.get(
    "/", response_model=list[AvailabilityOutSchema], status_code=status.HTTP_200_OK
)
async def get_availabilities(
    provider_id: UUID,
    limit: int = Query(
        20, gt=0, le=100, description="limiting the number of items to retrieve"
    ),
    skip: int = Query(0, ge=0, description="use for paginating based on passed items"),
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    availabilities = await availability_service.list_availability(
        db, provider_id, skip, limit
    )
    return availabilities


@router.delete("/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability(
    availability_id: UUID = Path(..., description="availability's id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    await availability_service.delete_availability(db, current_user, availability_id)
