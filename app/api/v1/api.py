from fastapi import APIRouter
from app.api.v1.endpoints import users
from app.schemas.healthcheck import Healthcheck

v1_router = APIRouter()


@v1_router.get("/healthcheck", response_model=Healthcheck)
async def healthcheck():
    return Healthcheck()


v1_router.include_router(users.router, tags=["Users"], prefix="/users")
