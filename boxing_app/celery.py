import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boxing_app.app_settings")

app = Celery("boxing_app")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-monday-morning': {
        'task': 'boxing_console.tasks.settle_order_task',
        'schedule': crontab(minute=10, hour=3) if settings.ENVIRONMENT == settings.PRODUCTION else crontab(),
        'args': [],
    },
    'judge-course-order-overdue': {
        'task': 'boxing_console.tasks.set_course_order_overdue',
        'schedule': crontab(minute=0, hour=0) if settings.ENVIRONMENT == settings.PRODUCTION else crontab(),
        'args': [],
    },
    'order-tear-finished-after-boxer-confirmed-7-days': {
        'task': 'boxing_console.tasks.order_tear_finished_after_boxer_confirmed',
        'schedule': crontab(minute=0, hour=0) if settings.ENVIRONMENT == settings.PRODUCTION else crontab(),
        'args': []
    },
    'refund-after-order-overdue': {
        'task': 'boxing_console.tasks.refund_after_order_overdue',
        'schedule': crontab(minute=0, hour=0) if settings.ENVIRONMENT == settings.PRODUCTION else crontab(),
        'args': []
    }

}
