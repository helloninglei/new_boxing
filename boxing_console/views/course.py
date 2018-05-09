from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import Course
from boxing_console.filters import CourseFilter
from boxing_console.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    filter_class = CourseFilter
    search_fields = ('boxer__real_name', 'boxer__mobile')
