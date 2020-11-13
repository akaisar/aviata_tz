from app.crud.base import CRUDBase

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    pass


ticket = CRUDTicket(Ticket)
