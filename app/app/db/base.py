# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.post import Post
from app.models.ticket import Ticket
from app.models.iata import IATA
