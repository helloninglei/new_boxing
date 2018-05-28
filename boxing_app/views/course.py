# -*- coding: utf-8 -*-
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets

from biz import redis_client
from biz.models import Course, BoxerIdentification, BoxingClub
from boxing_app.serializers import CourseAllowNullDataSerializer, CourseFullDataSerializer


class BoxerMyCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllowNullDataSerializer

    def get_queryset(self):
        return Course.objects.filter(boxer__user=self.request.user)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        validity = request.data.get('validity')
        club_id = request.data.get('club')
        club = get_object_or_404(BoxingClub, id=club_id)
        for course_data in request.data.get('course_list'):
            is_open = course_data.get('is_open')
            course = Course.objects.get(id=course_data.get('course_id'))
            course_data.pop('course_id')
            course_data['validity'] = validity
            course_data['club'] = club_id
            if is_open:
                serializer = CourseFullDataSerializer(instance=course, data=course_data)
            else:
                serializer = CourseAllowNullDataSerializer(instance=course, data=course_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(boxer=boxer)
        redis_client.record_object_location(boxer, club.longitude, club.latitude)
        return redirect('/boxer/course')
