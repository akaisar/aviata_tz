from fastapi import APIRouter
from app.api.v1.endpoints import posts, tickets

router = APIRouter()

router.include_router(posts.router, prefix="/post")
router.include_router(tickets.router, prefix="/ticket")
