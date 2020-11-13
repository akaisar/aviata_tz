from fastapi import APIRouter
from app.api.v1.endpoints import tickets

router = APIRouter()

router.include_router(tickets.router, prefix="/ticket")
