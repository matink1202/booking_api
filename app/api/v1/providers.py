from uuid import UUID

from fastapi import APIRouter, Depends, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User as UserModel
from app.schemas.provider import (
    ProviderCreateSchema,
    ProviderOutSchema,
    ProviderUpdateSchema,
)
from app.services import provider_service

router = APIRouter(tags=["Providers"], prefix="/providers")


@router.post("/", response_model=ProviderOutSchema, status_code=status.HTTP_201_CREATED)
async def create_provider_profile(
    request: ProviderCreateSchema,
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):

    provider = await provider_service.create_provider_profile(db, current_user, request)
    return provider


@router.get("/", response_model=list[ProviderOutSchema], status_code=status.HTTP_200_OK)
async def get_providers(
    limit: int = Query(
        20, gt=0, le=100, description="limiting the number of items to retrieve"
    ),
    skip: int = Query(0, ge=0, description="use for paginating based on passed items"),
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    providers = await provider_service.list_providers(db, skip, limit)
    return providers


@router.get(
    "/{provider_id}", response_model=ProviderOutSchema, status_code=status.HTTP_200_OK
)
async def get_provider_detail(
    provider_id: UUID = Path(...),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
):
    provider = await provider_service.get_provider(db, provider_id)
    return provider


@router.patch(
    "/{provider_id}", response_model=ProviderOutSchema, status_code=status.HTTP_200_OK
)
async def update_provider(
    request: ProviderUpdateSchema,
    provider_id: UUID = Path(...),  # noqa: B008
    db: AsyncSession = Depends(get_db),  # noqa: B008
    current_user: UserModel = Depends(get_current_user),  # noqa: B008
):
    provider = await provider_service.update_provider(
        db, current_user, provider_id, request
    )
    return provider
