# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import Count, Avg
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from biz import redis_client
from biz.models import Course, BoxerIdentification, BoxingClub, CourseOrder, OrderComment
from boxing_app.permissions import IsBoxerPermission
from boxing_app.serializers import CourseAllowNullDataSerializer, CourseFullDataSerializer


class BoxerMyCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllowNullDataSerializer
    permission_classes = (permissions.IsAuthenticated, IsBoxerPermission)

    def get_queryset(self):
        return Course.objects.filter(boxer__user=self.request.user)\
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
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        course = self.get_queryset().filter(is_open=True).last()
        response = super().list(request, *args, **kwargs)
        base_info = self.get_base_info(course=course, boxer=boxer)
        response.data.update(base_info)
        return response

    @classmethod
    def get_base_info(cls, course, boxer):
        base_info = {}
        comment_count_and_avg_score = OrderComment.objects.filter(order__boxer=boxer)\
            .aggregate(comments_count=Count('id'), avg_score=Avg('score'))
        base_info.update(comment_count_and_avg_score)
        base_info['order_count'] = CourseOrder.objects.filter(boxer=boxer).count()
        base_info['allowed_course'] = boxer.allowed_course
        if course:
            base_info['validity'] = course.validity
            base_info['boxer_id'] = course.boxer_id
            if course.club:
                base_info['club_id'] = course.club.id
                base_info['club_name'] = course.club.name
                base_info['club_city'] = course.club.city
                base_info['club_address'] = course.club.address
                base_info['club_longitude'] = course.club.longitude
                base_info['club_latitude'] = course.club.latitude
        return base_info


class GetBoxerCourseByAnyOneViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseAllowNullDataSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Course.objects.filter(boxer__id=self.kwargs['boxer_id'], is_open=True)\
            .annotate(order_count=Count('course_orders'), score=Avg('course_orders__comment__score'))\
            .select_related('club', 'boxer')

    def opened_courses_list(self, request, *args, **kwargs):
        boxer = BoxerIdentification.objects.get(id=kwargs['boxer_id'])
        course = self.get_queryset().filter(is_open=True).last()
        response = super().list(request, *args, **kwargs)
        base_info = BoxerMyCourseViewSet.get_base_info(course=course, boxer=boxer)
        response.data.update(base_info)
        return response
