# -*- coding: utf-8 -*-
from rest_framework import viewsets
from django.db.models import Count
from biz import models
from boxing_console import serializers
from biz.services.push_service import broadcast_news


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments')).prefetch_related('operator')

    def perform_create(self, serializer):
        news = serializer.save()
        if news.push_news:
            broadcast_news(news)

    perform_update = perform_create
