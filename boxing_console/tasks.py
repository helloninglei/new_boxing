from celery import shared_task
from datetime import datetime

from django.db.models import Q

from biz import constants
from biz.constants import MONEY_CHANGE_TYPE_INCREASE_ORDER_OVERDUE, DELAY_SEVEN_DAYS
from biz.models import CourseSettleOrder, CourseOrder
from biz.services.money_balance_service import change_money


@shared_task()
def settle_order_task():
    for order in CourseSettleOrder.objects.filter(settled=False, created_time__lt=datetime.now() - DELAY_SEVEN_DAYS):
        order.settle_order()


@shared_task()
def set_course_order_overdue():
    overdue_orders = CourseOrder.objects.filter(Q(course_validity__lt=datetime.today(),
                                                confirm_status=constants.COURSE_ORDER_STATUS_NOT_CONFIRMED)
                                                )
    for course_order in overdue_orders:
        course_order.set_overdue()


@shared_task()
def order_tear_finished_after_boxer_confirmed():
    course_sets = CourseOrder.objects.filter(confirm_status=constants.COURSE_ORDER_STATUS_BOXER_CONFIRMED,
                                             boxer_confirm_time__lt=datetime.now() - DELAY_SEVEN_DAYS)
    for course_order in course_sets:
        CourseSettleOrder.objects.get_or_create(course=course_order.course,
                                                order=course_order.pay_order,
                                                course_order=course_order)
    course_sets.update(status=constants.COURSE_PAYMENT_STATUS_WAIT_COMMENT)


@shared_task()
def refund_after_order_overdue():
    should_refund_orders = CourseOrder.objects.filter(status=constants.COURSE_PAYMENT_STATUS_OVERDUE,
                                                      course_validity__lt=datetime.now() - DELAY_SEVEN_DAYS,
                                                      refund_record__isnull=True)
    for course_order in should_refund_orders:
        insurance_amount = course_order.insurance_amount or 0
        return_amount = course_order.amount - insurance_amount
        change_money_log = change_money(course_order.user, return_amount, MONEY_CHANGE_TYPE_INCREASE_ORDER_OVERDUE,
                                        course_order.order_number)
        course_order.refund_record = change_money_log
        course_order.save()
