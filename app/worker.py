import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

celery_app.conf.beat_schedule = {
    "collect-prices-every-minute": {
        "task": "app.tasks.collect_prices",
        "schedule": crontab(minute="*")
    },
}

celery_app.autodiscover_tasks(["app"])
