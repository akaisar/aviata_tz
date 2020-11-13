from celery import Celery
from celery.schedules import crontab

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.beat_schedule = {
    'caching': {
        'task': 'tasks.caching',
        'schedule': crontab(hour=16, minute=17),
    },
}
