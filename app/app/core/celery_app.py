from celery import Celery
from celery.schedules import crontab

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.beat_schedule = {
    "reload_cache": {
        "task": "tasks.reload_cache",
        "schedule": crontab(hour=0, minute=0),
    },
}
