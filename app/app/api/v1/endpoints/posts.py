from typing import List, Optional

from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from starlette.responses import UJSONResponse

from app import crud
from app.api.utils.db import get_db
from app.api.utils.errors import NotFoundSchema, NotFound
from app.schemas.post import Post


router = APIRouter()


@router.get("/", response_model=List[Post], response_class=UJSONResponse)
def list_posts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    posts = crud.post.get_multi(db, skip=skip, limit=limit)
    return posts


@router.get(
    "/{post_id}/",
    response_model=Post,
    responses={404: {"model": NotFoundSchema}},
    response_class=UJSONResponse,
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = crud.post.get(db, post_id)
    if not post:
        return NotFound(message="Post not found")
    return post
