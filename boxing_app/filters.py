import django_filters

from biz.models import BoxerIdentification


class NearbyBoxerFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(name='course__price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(name='course__price', lookup_expr='lte')
    course_name = django_filters.CharFilter('course__course_name')

    class Meta:
        model = BoxerIdentification
        fields = ["min_price", "max_price", "course_name"]
