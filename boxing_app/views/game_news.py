# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Count, F
from biz import models
from biz.utils import get_device_platform
from boxing_app import serializers

h5_base_url = settings.SHARE_H5_BASE_URL


@api_view(['GET'])
def get_news_url(request, pk):
    if get_device_platform(request):
        models.GameNews.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
    return Response({'url': f'{h5_base_url}game_news/{pk}/1'})  # 1 在app内打开


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    permission_classes = (AllowAny,)
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments'))
