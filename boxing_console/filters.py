# -*- coding: utf-8 -*-
import datetime

import django_filters

from biz import models


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

