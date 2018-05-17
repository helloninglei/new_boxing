from django.contrib.contenttypes.models import ContentType
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import Course, PayOrder
from boxing_console.filters import CourseFilter, CourseOrderFilter
from boxing_console.serializers import CourseSerializer, CourseOrderSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_class = CourseFilter
    search_fields = ('boxer__real_name', 'boxer__mobile')


class CourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderSerializer
    queryset = PayOrder.objects.filter(content_type=ContentType.objects.get_for_model(Course))
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('user__mobile', 'course__boxer__real_name', 'course__boxer__mobile')
    filter_class = CourseOrderFilter
