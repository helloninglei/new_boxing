# -*- coding: utf-8 -*-
from rest_framework import mixins, viewsets, permissions

from biz.models import  BoxerIdentification
from boxing_app.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(mixins.CreateModelMixin,
                                 mixins.RetrieveModelMixin,
                                  viewsets.GenericViewSet):
    serializer_class = BoxerIdentificationSerializer

    def get_object(self):
        return BoxerIdentification.objects.filter(user=self.request.user).first()