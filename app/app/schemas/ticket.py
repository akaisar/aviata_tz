from datetime import datetime, date

from pydantic import BaseModel

from app.schemas.iata import IATABase

from typing import Optional


class TicketBase(BaseModel):
    date_from: datetime
    date_to: datetime
    price: int
    booking_token: str
    date_search: date


class TicketCreate(TicketBase):
    pass


class TicketUpdate(TicketBase):
    pass


class TicketInDB(TicketBase):
    id: int

    class Config:
        orm_mode = True


class Ticket(TicketInDB):
    pass
