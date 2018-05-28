from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import Course, PayOrder, CourseSettleOrder
from boxing_console.filters import CourseFilter, CourseOrderFilter, CourseSettleOrderFilter
from boxing_console.serializers import CourseSerializer, CourseOrderSerializer, CourseSettleOrderSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = CourseFilter
    search_fields = ('boxer__real_name', 'boxer__mobile')


class CourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('user__mobile', 'course__boxer__real_name', 'course__boxer__mobile')
    filter_class = CourseOrderFilter

    def get_queryset(self):
        return PayOrder.objects.filter(content_type=ContentType.objects.get_for_model(Course))


class CourseSettleOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSettleOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CourseSettleOrderFilter
    queryset = CourseSettleOrder.objects.all().prefetch_related('course', 'order', 'order__user', 'course__boxer')
