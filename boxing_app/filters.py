import django_filters
from biz.models import MoneyChangeLog
from django.db.models import F


class MoneyChangeLogFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method="filter_keyword")

    def filter_keyword(self, qs, name, value):
        if value == "income":
            return qs.filter(last_amount__lt=F("remain_amount"))
        if value == "expend":
            return qs.filter(last_amount__gt=F("remain_amount"))
        return qs

    class Meta:
        model = MoneyChangeLog
        fields = ['keyword']
