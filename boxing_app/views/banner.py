# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from biz import models
from boxing_app.serializers import BannerSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = (AllowAny,)
    serializer_class = BannerSerializer
    queryset = models.Banner.objects.all()
