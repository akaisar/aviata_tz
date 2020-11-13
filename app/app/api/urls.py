from fastapi import APIRouter
from .v1.urls import router as v1_router


root_router = APIRouter()
root_router.include_router(v1_router, prefix="/v1")
