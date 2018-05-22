# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from rest_framework import viewsets

from biz.models import Course, BoxerIdentification
from boxing_app.serializers import CourseAllowNullDataSerializer, CourseFullDataSerializer


class BoxerMyCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllowNullDataSerializer

    def get_queryset(self):
        return Course.objects.filter(boxer__user=self.request.user)

    def update(self, request, *args, **kwargs):
        for course_data in request.data.get('course_list'):
            is_open = course_data.get('is_open')
            course = Course.objects.get(id=course_data.get('course_id'))
            boxer = BoxerIdentification.objects.get(user=self.request.user)
            course_data.pop('course_id')
            course_data['validity'] = request.data.get('validity')
            course_data['club'] = request.data.get('club')
            if is_open:
                serializer = CourseFullDataSerializer(instance=course, data=course_data)
            else:
                serializer = CourseAllowNullDataSerializer(instance=course, data=course_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(boxer=boxer)
        return redirect('/boxer/course')
