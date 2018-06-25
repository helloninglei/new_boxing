import django_filters
from biz.models import MoneyChangeLog, Course

from biz.models import BoxerIdentification


class NearbyBoxerFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name='m_price', lookup_expr='gt')
    max_price = django_filters.NumberFilter(name='m_price', lookup_expr='lte')
    course_name = django_filters.CharFilter(method='filter_course_name')
    city = django_filters.CharFilter('course__club__city')

    def filter_course_name(self, qs, name, value):
        courses_qs = Course.objects.filter(course_name=value, is_open=True).select_related('boxer')
        boxer_id_set = set(course.boxer.id for course in courses_qs)
        return qs.filter(id__in=boxer_id_set)

    class Meta:
        model = BoxerIdentification
        fields = ["min_price", "max_price", "course_name", "city"]


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
