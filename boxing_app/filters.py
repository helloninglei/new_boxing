import django_filters
from biz.models import MoneyChangeLog


class MoneyChangeLogFilter(django_filters.FilterSet):
    keyword = django_filters.CharFilter(method="filter_keyword")

    def filter_keyword(self, qs, name, value):
        if value == "income":
            return qs.filter(change_amount__gt=0)
        if value == "expend":
            return qs.filter(change_amount__lt=0)
        return qs

    class Meta:
        model = MoneyChangeLog
        fields = ['keyword']
