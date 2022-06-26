from fastapi import FastAPI
from app.api.v1.api import v1_router

app = FastAPI()

app.include_router(v1_router, tags=["v1"], prefix="/api/v1")
