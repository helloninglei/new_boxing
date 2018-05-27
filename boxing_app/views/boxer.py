# -*- coding: utf-8 -*-
from django.db.models import Case, When
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from biz import constants, redis_client
from biz.models import BoxerIdentification
from boxing_app.serializers import BoxerIdentificationSerializer, OrderdBoxerIdentificationSerializer


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


class OrderdBoxerListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderdBoxerIdentificationSerializer

    def get_queryset(self):
        longitude = self.request.data.get('longitude')
        latitude = self.request.data.get('latitude')
        boxer_id_list = redis_client.get_near_object(BoxerIdentification, longitude, latitude)
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(boxer_id_list)])
        return  BoxerIdentification.objects.filter(id__in=boxer_id_list).order_by(preserved)

