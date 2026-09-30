from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.user import User as UserModel
from app.models.user import UserRole
from app.schemas.services import (
    ServiceCreateSchema,
    ServiceOutSchema,
    ServiceUpdateSchema,
)
from app.services import service_service

router = APIRouter(tags=["Services"], prefix="/services")


@router.post("/", response_model=ServiceOutSchema, status_code=status.HTTP_201_CREATED)
async def create_service(
    request: ServiceCreateSchema,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(require_roles(UserRole.ADMIN, UserRole.PROVIDER)),  # noqa: B008
):
    service = await service_service.create_service(db, current_user, request)
    return service


@router.get("/", response_model=list[ServiceOutSchema], status_code=status.HTTP_200_OK)
async def get_services(
    provider_id: UUID | None = None,
    limit: int = Query(
        20, gt=0, le=100, description="limiting the number of items to retrieve"
    ),
    skip: int = Query(0, ge=0, description="use for paginating based on passed items"),
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    services = await service_service.list_services(db, skip, limit, provider_id)
    return services


@router.get(
    "/{service_id}", response_model=ServiceOutSchema, status_code=status.HTTP_200_OK
)
async def get_service_detail(
    service_id: UUID = Path(..., description="service id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    service = await service_service.get_service(db, service_id)
    return service


@router.patch(
    "/{service_id}", response_model=ServiceOutSchema, status_code=status.HTTP_200_OK
)
async def update_service(
    request: ServiceUpdateSchema,
    service_id: UUID = Path(..., description="service id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    service = await service_service.update_service(
        db, current_user, service_id, request
    )
    return service


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: UUID = Path(..., description="service id"),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    await service_service.delete_service(db, current_user, service_id)
