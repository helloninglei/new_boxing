import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boxing_app.app_settings")

app = Celery("boxing_app")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'boxing_console.tasks.settle_order_task',
        'schedule': crontab(minute=10, hour=3),
        'args': [],
    },
}
