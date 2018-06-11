from celery import shared_task
from datetime import datetime, timedelta

from biz import constants
from biz.models import CourseSettleOrder, CourseOrder


@shared_task()
def settle_order_task():
    for order in CourseSettleOrder.objects.filter(settled=False, created_time__lt=datetime.now() - timedelta(days=7)):
        order.settle_order()


@shared_task()
def set_course_order_overdue():
    overdue_orders = CourseOrder.objects.filter(course_validity__lt=datetime.date,
                                                confirm_status=constants.COURSE_ORDER_STATUS_NOT_CONFIRMED)
    for course_order in overdue_orders:
        course_order.set_overdue()
