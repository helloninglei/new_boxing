# -*- coding: utf-8 -*-
import datetime

import django_filters
from django.db.models import Q

from biz import models
from biz.models import Course
from biz import constants
from biz.constants import REPORT_STATUS_NOT_PROCESSED


class CommonFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name='created_time', lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(method='filter_end_time')

    def filter_end_time(self, qs, name, value):
        if value:
            next_day = value + datetime.timedelta(days=1)
            return qs.filter(created_time__lt=next_day)

        return qs.filter()


class CoinChangLogListFilter(CommonFilter):
    class Meta:
        model = models.CoinChangeLog
        fields = ['user', 'operator', 'change_type', 'created_time', 'start_time', 'end_time']


class CourseFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(name='price', lookup_expr='lte')
    is_accept_order = django_filters.CharFilter(method='filter_is_accept_order')

    def filter_is_accept_order(self, qs, name, value):
        if value:
            return qs.filter(~Q(boxer__is_locked=value))
        return qs.filter()

    class Meta:
        model = Course
        fields = ['price_min', 'price_max', 'course_name', 'is_accept_order']


class HotVideoFilter(CommonFilter):
    class Meta:
        model = models.HotVideo
        fields = ('created_time',)


class GameNewsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(name='created_time', lookup_expr='gte')
    end_date = django_filters.DateFilter(name='created_time', lookup_expr='lte')

    class Meta:
        model = models.GameNews
        fields = ('start_date', 'end_date')


class CourseOrderFilter(CommonFilter):
    pay_time_start = django_filters.DateTimeFilter(name='pay_time', lookup_expr='gte')
    pay_time_end = django_filters.DateTimeFilter(name='pay_time', lookup_expr='lte')

    class Meta:
        model = models.PayOrder
        fields = ['pay_time_start', 'pay_time_end', 'course__course_name', 'payment_type', 'status']


class UserFilter(django_filters.FilterSet):
    is_boxer = django_filters.CharFilter(method="filter_user_type")
    start_time = django_filters.DateTimeFilter(name="date_joined", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(name="date_joined", lookup_expr="lte")

    def filter_user_type(self, qs, name, value):

        if value == "true":
            return qs.filter(boxer_identification__authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED)
        if value == "false":
            return qs.filter(
                ~Q(boxer_identification__authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED))
        return qs

    class Meta:
        model = models.User
        fields = ["is_boxer", "start_time", "end_time"]


class ReportFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='filter_status')

    def filter_status(self, qs, name, value):
        if value == 'unprocessed':
            condition = {
                'status': REPORT_STATUS_NOT_PROCESSED
            }
        else:
            condition = {
                'status__gt': REPORT_STATUS_NOT_PROCESSED
            }

        return qs.filter(**condition)

    class Meta:
        model = models.Report
        fields = ['status']


class CourseSettleOrderFilter(django_filters.FilterSet):
    buyer = django_filters.CharFilter(name='order__user__mobile')
    boxer = django_filters.CharFilter(method='boxer_filter')
    start_date = django_filters.DateFilter(name='settled_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(name='settled_date', lookup_expr='lte')
    course = django_filters.CharFilter(method='course_filter')
    status = django_filters.CharFilter(method='status_filter')

    def course_filter(self, qs, name, value):
        value = value.lower()
        if value == 'all':
            return qs
        return qs.filter(course__course_name=value)

    def status_filter(self, qs, name, value):
        value = value.lower()
        if value == 'settled':
            return qs.filter(settled=True)
        elif value == 'unsettled':
            return qs.filter(settled=False)
        return qs

    def boxer_filter(self, qs, name, value):
        return qs.filter(Q(course__boxer__real_name=value) | Q(course__boxer__mobile=value))

    class Meta:
        model = models.CourseSettleOrder
        fields = ('buyer', 'boxer', 'start_date', 'end_date', 'course', 'status')


class WithdrawLogFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method="status_filter")

    def status_filter(self, qs, name, value):
        if value.lower() == "waiting":
            return qs.filter(status=constants.WITHDRAW_STATUS_WAITING)
        if value.lower() == "finished":
            return qs.filter(~Q(status=constants.WITHDRAW_STATUS_WAITING))
        if value.lower() == "approved":
            return qs.filter(status=constants.WITHDRAW_STATUS_APPROVED)
        if value.lower() == "rejected":
            return qs.filter(status=constants.WITHDRAW_STATUS_REJECTED)
        return qs

    class Meta:
        model = models.WithdrawLog
        fields = ("status",)


class MoneyChangeLogFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(name="created_time", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(name="created_time", lookup_expr="lte")

    class Meta:
        model = models.MoneyChangeLog
        fields = ("start_time", "end_time")
