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

    def retrieve(self, request, *args, **kwargs):
        instance = BoxerIdentification.objects.filter(user=kwargs['pk']).first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        else:
            return Response(data={'message':'拳手认证信息不存在'},status=status.HTTP_400_BAD_REQUEST)
