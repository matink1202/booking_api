from fastapi import APIRouter

from app.api.v1 import appointments, auth, availability, providers, services

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(services.router)
api_router.include_router(providers.router)
api_router.include_router(appointments.router)
api_router.include_router(availability.router)