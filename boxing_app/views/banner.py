# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from biz import models
from boxing_app.serializers import BannerSerializer


class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = []
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = BannerSerializer
    queryset = models.Banner.objects.all()
