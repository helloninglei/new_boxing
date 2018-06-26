# -*- coding: utf-8 -*-
from django.db import transaction
from django.db.models import Count, Avg, Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response

from biz import redis_client
from biz.constants import COURSE_PAYMENT_STATUS_UNPAID
from biz.models import Course, BoxerIdentification, BoxingClub, CourseOrder, OrderComment
from boxing_app.permissions import IsBoxerPermission
from boxing_app.serializers import CourseAllowNullDataSerializer, CourseFullDataSerializer


class BoxerMyCourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseAllowNullDataSerializer
    permission_classes = (permissions.IsAuthenticated, IsBoxerPermission)

    def get_queryset(self):
        return Course.objects.filter(boxer__user=self.request.user)\
            .annotate(order_count=Count('course_orders',
                                        filter=Q(course_orders__status__gt=COURSE_PAYMENT_STATUS_UNPAID)),
                      score=Avg('course_orders__comment__score'))\
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
        response = super().list(request, *args, **kwargs)
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        if boxer.is_locked:
            return Response({'message': '你暂时不能接单。'}, status=status.HTTP_400_BAD_REQUEST)
        self.get_boxer_base_info(dict=response.data, boxer=boxer)
        course = self.get_queryset().filter(is_open=True).select_related('club').last()
        if course:
            self.get_course_base_info(dict=response.data, course=course)
        return response

    @staticmethod
    def get_course_base_info(dict, course):
        dict['validity'] = course.validity
        dict['boxer_id'] = course.boxer_id
        dict['club_id'] = course.club.id
        dict['club_name'] = course.club.name
        dict['club_city'] = course.club.city
        dict['club_address'] = course.club.address
        dict['club_longitude'] = course.club.longitude
        dict['club_latitude'] = course.club.latitude
        return dict

    @staticmethod
    def get_boxer_base_info(dict, boxer):
        dict['order_count'] = CourseOrder.objects.filter(boxer=boxer, status__gt=COURSE_PAYMENT_STATUS_UNPAID).count()
        dict['allowed_course'] = boxer.allowed_course
        comment_count_and_avg_score = OrderComment.objects.filter(order__boxer=boxer) \
            .aggregate(comments_count=Count('id'), avg_score=Avg('score'))
        dict.update(comment_count_and_avg_score)
        return dict


class GetBoxerCourseByAnyOneViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseAllowNullDataSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Course.objects.filter(boxer__id=self.kwargs['boxer_id'], is_open=True)\
            .annotate(order_count=Count('course_orders',
                                        filter=Q(course_orders__status__gt=COURSE_PAYMENT_STATUS_UNPAID)),
                      score=Avg('course_orders__comment__score'))\
            .select_related('club', 'boxer')

    def opened_courses_list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        boxer = BoxerIdentification.objects.get(id=kwargs['boxer_id'])
        course = self.get_queryset().select_related('club').last()
        BoxerMyCourseViewSet.get_course_base_info(dict=response.data, course=course)
        BoxerMyCourseViewSet.get_boxer_base_info(dict=response.data, boxer=boxer)
        return response
