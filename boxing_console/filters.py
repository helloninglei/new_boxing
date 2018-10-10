# -*- coding: utf-8 -*-
import datetime

import django_filters
from django.db.models import Q

from biz import models
from biz.models import Course
from biz import constants
from biz.constants import REPORT_STATUS_NOT_PROCESSED, PAYMENT_STATUS_UNPAID, USER_TYPE_CHOICE, HOT_VIDEO_USER_ID


class CommonFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name='created_time', lookup_expr='gte')
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
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    is_accept_order = django_filters.CharFilter(method='filter_is_accept_order')

    def filter_is_accept_order(self, qs, name, value):
        if value:
            return qs.filter(~Q(boxer__is_locked=value))
        return qs

    class Meta:
        model = Course
        fields = ['price_min', 'price_max', 'course_name', 'is_accept_order']


class HotVideoFilter(CommonFilter):
    search = django_filters.CharFilter(method='search_filter')
    tag = django_filters.ChoiceFilter(choices=constants.HOT_VIDEO_TAG_CHOICES, field_name='tag')
    is_hot = django_filters.CharFilter(method='is_hot_filter')
    is_need_pay = django_filters.CharFilter(method='is_need_pay_filter')

    def is_hot_filter(self, qs, name, value=''):
        value = value.lower()
        if value == 'yes':
            return qs.filter(users__in=[HOT_VIDEO_USER_ID])
        elif value == 'no':
            return qs.filter(~Q(users__in=[HOT_VIDEO_USER_ID]))
        else:
            return qs

    def is_need_pay_filter(self, qs, name, value=''):
        value = value.lower()
        if value == 'yes':
            return qs.filter(price__gt=0)
        elif value == 'no':
            return qs.filter(price=0)
        else:
            return qs

    def search_filter(self, qs, name, value):
        if value.isdigit():
            return qs.filter(Q(name__icontains=value) | Q(users__id=value) | Q(pk=value))
        return qs.filter(Q(name__icontains=value) | Q(users__user_profile__nick_name__contains=value))

    class Meta:
        model = models.HotVideo
        fields = ('start_time', 'end_time', 'search', 'is_hot')


class GameNewsFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='updated_time', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='updated_time', lookup_expr='lte')
    stay_top = django_filters.CharFilter(method='filter_stay_top')

    def filter_stay_top(self, qs, name, value):
        value = value.lower()
        if value == 'true':
            return qs.filter(stay_top=True)
        if value == 'false':
            return qs.filter(stay_top=False)
        return qs

    class Meta:
        model = models.GameNews
        fields = ('start_date', 'end_date', 'stay_top')


class CourseOrderFilter(CommonFilter):
    pay_time_start = django_filters.DateTimeFilter(field_name='pay_time', lookup_expr='gte')
    pay_time_end = django_filters.DateTimeFilter(field_name='pay_time', lookup_expr='lte')

    class Meta:
        model = models.CourseOrder
        fields = ['pay_time_start', 'pay_time_end', 'course_name', 'pay_order__payment_type', 'status']


class UserFilter(django_filters.FilterSet):
    user_type = django_filters.CharFilter(method="filter_user_type")
    start_time = django_filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="date_joined", lookup_expr="lte")

    def filter_user_type(self, qs, name, value):
        if not value:
            return qs
        if value == "4":
            return qs.filter(user_type__isnull=True)
        return qs.filter(user_type=value)

    class Meta:
        model = models.User
        fields = ["user_type", "start_time", "end_time"]


class ReportFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method='filter_status')

    def filter_status(self, qs, name, value):
        if value == 'unprocessed':
            return qs.filter(status=REPORT_STATUS_NOT_PROCESSED)
        return qs.filter(status__gt=REPORT_STATUS_NOT_PROCESSED)

    class Meta:
        model = models.Report
        fields = ('status',)


class CourseSettleOrderFilter(django_filters.FilterSet):
    buyer = django_filters.CharFilter(field_name='order__user__mobile')
    boxer = django_filters.CharFilter(method='boxer_filter')
    start_date = django_filters.DateFilter(field_name='settled_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='settled_date', lookup_expr='lte')
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
        return qs.filter(Q(course__boxer__real_name=value) | Q(course__boxer__user__mobile=value))

    class Meta:
        model = models.CourseSettleOrder
        fields = ('buyer', 'boxer', 'start_date', 'end_date', 'course', 'status')


class WithdrawLogFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(method="status_filter")

    def status_filter(self, qs, name, value):
        value = value.lower()
        if value == "waiting":
            return qs.filter(status=constants.WITHDRAW_STATUS_WAITING)
        if value == "finished":
            return qs.filter(~Q(status=constants.WITHDRAW_STATUS_WAITING))
        if value == "approved":
            return qs.filter(status=constants.WITHDRAW_STATUS_APPROVED)
        if value == "rejected":
            return qs.filter(status=constants.WITHDRAW_STATUS_REJECTED)
        return qs

    class Meta:
        model = models.WithdrawLog
        fields = ("status",)


class MoneyChangeLogFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name="created_time", lookup_expr="gte")
    end_time = django_filters.DateTimeFilter(field_name="created_time", lookup_expr="lte")

    class Meta:
        model = models.MoneyChangeLog
        fields = ("start_time", "end_time")


class PayOrderFilter(django_filters.FilterSet):
    device = django_filters.CharFilter(field_name="device")
    payment_type = django_filters.CharFilter(field_name="payment_type")
    status = django_filters.CharFilter(method="status_filter")

    def status_filter(self, qs, name, value):
        if not value:
            return qs
        if value == "1":
            return qs.filter(status=PAYMENT_STATUS_UNPAID)
        if value == "2":
            return qs.filter(~Q(status=PAYMENT_STATUS_UNPAID))
        return self.Meta.model.objects.none()

    class Meta:
        model = models.PayOrder
        fields = ["device", "payment_type", "status"]


class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_time', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='created_time', lookup_expr='lte')
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    user_type = django_filters.ChoiceFilter(choices=USER_TYPE_CHOICE, field_name='user__user_type')

    class Meta:
        model = models.Message
        fields = ('start_date', 'end_date', 'content', 'user_type')
