# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from django.db.models import Count, Sum
from django.utils import timezone
from biz import models
from boxing_console import serializers
from biz.services.push_service import broadcast_news
from boxing_console.filters import GameNewsFilter


class NewsViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.NewsSerializer
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments')).order_by(
        '-updated_time').prefetch_related('operator')
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = GameNewsFilter
    search_fields = ('title',)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data.update(self.filter_queryset(self.get_queryset()).aggregate(real_views_amount=Sum("views_count")))
        return response

    def perform_create(self, serializer):
        news = serializer.save(updated_time=timezone.now())
        if news.push_news:
            broadcast_news(news)

    perform_update = perform_create
