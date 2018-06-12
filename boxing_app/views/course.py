# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from biz import redis_client
from biz.models import Course, BoxerIdentification, BoxingClub, CourseOrder
from boxing_app.serializers import CourseAllowNullDataSerializer, CourseFullDataSerializer


class BoxerMyCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllowNullDataSerializer
    permission_classes = (permissions.AllowAny,)
    condition = {}

    def get_queryset(self):
        return Course.objects.filter(**self.condition)\
            .annotate(order_count=Count('course_orders'), score=Avg('course_orders__comment__score'))\
            .select_related('club', 'boxer')

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
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        BoxerMyCourseViewSet.condition = {"boxer__user": self.request.user}
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        kwargs['boxer'] = boxer
        return self.perform_list(request, *args, **kwargs)

    def opened_courses_list(self, request, *args, **kwargs):
        BoxerMyCourseViewSet.condition = {"boxer__id": kwargs['boxer_id'], "is_open": True}
        boxer = BoxerIdentification.objects.get(id=kwargs['boxer_id'])
        kwargs['boxer'] = boxer
        return self.perform_list(request, *args, **kwargs)

    def perform_list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        com_count_and_avg_score = self.get_queryset().aggregate(comments_count=Count("course_orders__comment"),
                                                                avg_score=Avg("course_orders__comment__score"))
        course = self.get_queryset().filter(is_open=True).last()
        common_info = self.get_comment_info(course=course, boxer=kwargs['boxer'])
        response.data.update(common_info)
        response.data.update(com_count_and_avg_score)
        return response

    @staticmethod
    def get_comment_info(course, boxer):
        comment_info = {}
        comment_info['order_count'] = CourseOrder.objects.filter(boxer=boxer).count()
        comment_info['allowed_course'] = boxer.allowed_course
        if course:
            comment_info['validity'] = course.validity
            comment_info['boxer_id'] = course.boxer_id
            if course.club:
                comment_info['club_id'] = course.club.id
                comment_info['club_name'] = course.club.name
                comment_info['club_city'] = course.club.city
                comment_info['club_address'] = course.club.address
                comment_info['club_longitude'] = course.club.longitude
                comment_info['club_latitude'] = course.club.latitude
        return comment_info
