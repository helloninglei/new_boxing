# -*- coding: utf-8 -*-
from rest_framework import viewsets
from biz import models
from boxing_app.serializers import BannerSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BannerSerializer
    queryset = models.Banner.objects.all()
