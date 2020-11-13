from datetime import datetime

from pydantic import BaseModel


class TicketResponse(BaseModel):
    fly_from: str
    fly_to: str
    date_from: datetime
    date_to: datetime
    price: int
