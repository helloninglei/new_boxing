# -*- coding: utf-8 -*-
from rest_framework import viewsets, filters
from biz import models
from boxing_console.serializers import BannerSerializer


class BannerViewSet(viewsets.ModelViewSet):
    serializer_class = BannerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    queryset = models.Banner.objects.all()
