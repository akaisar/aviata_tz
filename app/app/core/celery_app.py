from celery import Celery
from celery.schedules import crontab
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.beat_schedule = {
    "reload_cache": {
        "task": "app.worker.reload_cache",
        "schedule": crontab(hour=0, minute=0),
    },
}
