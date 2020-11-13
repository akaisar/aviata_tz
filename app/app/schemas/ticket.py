from datetime import datetime, date

from pydantic import BaseModel


class TicketBase(BaseModel):
    fly_from: str
    fly_to: str
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
