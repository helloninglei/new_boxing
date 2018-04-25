# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets, permissions

from biz.models import  BoxerIdentification
from boxing_app.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(mixins.CreateModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = BoxerIdentificationSerializer
    permission_classes = (permissions.AllowAny)

    def get_queryset(self):
        queryset = BoxerIdentification.objects.filter(user=self.request.user)
        return queryset