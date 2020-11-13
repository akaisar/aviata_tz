import datetime

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Ticket(Base):
    __tablename__ = "ticket"
    id = Column(Integer, primary_key=True, index=True)
    fly_from_id = Column(Integer, ForeignKey("iata.id"))
    fly_from = relationship("IATA", foreign_keys=[fly_from_id])
    fly_to_id = Column(Integer, ForeignKey("iata.id"))
    fly_to = relationship("IATA", foreign_keys=[fly_to_id])
    date_from = Column(DateTime)
    date_to = Column(DateTime)
    date_search = Column(Date)
    price = Column(Integer)
    booking_token = Column(String)
