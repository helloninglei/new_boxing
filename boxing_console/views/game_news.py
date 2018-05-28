# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from django.db.models import Count
from biz import models
from boxing_console import serializers
from biz.services.push_service import broadcast_news
from boxing_console.filters import CreateTimeFilter


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments')).prefetch_related('operator')
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = CreateTimeFilter
    search_fields = ('user__id', 'name')

    def perform_create(self, serializer):
        news = serializer.save()
        if news.push_news:
            broadcast_news(news)

    perform_update = perform_create
