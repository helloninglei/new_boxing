# -*- coding: utf-8 -*-
import datetime

import django_filters
from django.db.models import Q

from biz import models
from biz.models import Course
from biz import constants


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
        fields = ['created_time']


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
        boxer_user_ids = models.BoxerIdentification.objects.filter(
            authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED).values_list(*['user'], flat=True)

        if value == "true":
            return qs.filter(id__in=boxer_user_ids)
        if value == "false":
            return qs.filter(~Q(id__in=boxer_user_ids))
        return qs

    class Meta:
        model = models.User
        fields = ["is_boxer", "start_time", "end_time"]
