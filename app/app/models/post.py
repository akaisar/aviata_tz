import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime

from app.db.base_class import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String)
    content = Column(String)
    author = Column(String)
    tags_string = Column(String)

    time_published = Column(DateTime, default=datetime.datetime.utcnow)
    comments_count = Column(Integer, default=0)
    reading_count = Column(Integer, default=0)
    score = Column(Integer, default=0)

    is_tutorial = Column(Boolean(), default=False)
