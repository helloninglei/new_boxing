# -*- coding: utf-8 -*-
from django.db.models import Case, When, Count, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, filters
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from biz import constants, redis_client
from biz.models import BoxerIdentification
from boxing_app.filters import NearbyBoxerFilter
from boxing_app.serializers import BoxerIdentificationSerializer, NearbyBoxerIdentificationSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerIdentificationSerializer

    def get_object(self):
        return BoxerIdentification.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.authentication_state == constants.BOXER_AUTHENTICATION_STATE_WAITING:
            return Response({"message": "存在待审核的认证信息，不能修改"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NearbyBoxerListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = NearbyBoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.filter(course__is_open=True,
                                                  authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED,
                                                  is_locked=False).annotate(order_count=Count('course__orders'),
                                                                            course_min_price=Min('course__price')).prefetch_related('course')
    filter_backends = (DjangoFilterBackend,)
    filter_class = NearbyBoxerFilter

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        if longitude and latitude:
            boxer_id_list = redis_client.get_near_object(BoxerIdentification, longitude, latitude)
            sort_rule = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(boxer_id_list)])
            return super().get_queryset().filter(id__in=boxer_id_list).order_by(sort_rule)
        return super().get_queryset()
