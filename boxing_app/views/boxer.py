# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from biz.models import  BoxerIdentification
from boxing_app.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 viewsets.GenericViewSet):
    serializer_class = BoxerIdentificationSerializer

    def get_object(self):
        return BoxerIdentification.objects.filter(user=self.request.user).first()