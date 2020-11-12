from datetime import datetime

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    author: str
    tags_string: str

    is_tutorial: bool


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostInDB(PostBase):
    id: int
    time_published: datetime
    comments_count: int
    reading_count: int
    score: int

    class Config:
        orm_mode = True


class Post(PostInDB):
    pass
