from fastapi import APIRouter
from app.api.v1.endpoints import posts

router = APIRouter()

router.include_router(posts.router, prefix="/post")
