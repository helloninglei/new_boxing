from celery import shared_task
from datetime import datetime, timedelta
from biz.models import CourseSettleOrder


@shared_task()
def settle_order_task():
    for order in CourseSettleOrder.objects.filter(settled=False, created_time__lt=datetime.now() - timedelta(days=7)):
        order.settle_order()
