import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class IATA(Base):
    __tablename__ = 'iata'
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String)
