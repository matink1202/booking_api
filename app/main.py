from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("app start")
    yield
    print("app shut down")


app = FastAPI(title="Booking API", lifespan=lifespan)
app.include_router(api_router, prefix="/api/v1")