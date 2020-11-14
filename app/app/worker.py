from app.core.celery_app import celery_app
from app.models.ticket import Ticket
from app.models.iata import IATA
from app.core.celery_app import celery_app
from celery.task import periodic_task
from app.db.session import db_session
from celery.schedules import crontab
from app.core.caching import caching


@celery_app.task(acks_late=True)
def test_celery(word: str) -> str:
    return f"test task return {word}"


@celery_app.task
def reload_cache():
    tickets = db_session.query(Ticket).all()
    for ticket in tickets:
        db_session.delete(ticket)
    db_session.commit()
    caching()
