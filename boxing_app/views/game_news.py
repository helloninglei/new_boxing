# -*- coding: utf-8 -*-
from django.conf import settings
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Count, F
from biz import models
from biz.utils import get_device_platform
from boxing_app import serializers

h5_base_url = settings.SHARE_H5_BASE_URL


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    permission_classes = (AllowAny,)
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments'))

    def retrieve(self, request, *args, **kwargs):
        news_id = self.kwargs['pk']
        url = f'{h5_base_url}game_news/{news_id}'
        if get_device_platform(request):
            models.GameNews.objects.filter(pk=news_id).update(views_count=F('views_count') + 1)
            return redirect(url)
        return super().retrieve(request, *args, **kwargs)
