# -*- coding: utf-8 -*-
import datetime

import django_filters
from django.db.models import Q

from biz import models
from biz.models import Course


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
