import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boxing_app.app_settings")

app = Celery("boxing_app")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
