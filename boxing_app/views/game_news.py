# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.db.models import Count, F
from biz import models
from boxing_app import serializers


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    permission_classes = (AllowAny,)
    queryset = models.GameNews.objects.annotate(comment_count=Count('comments'))

    def retrieve(self, request, *args, **kwargs):
        # TODO  App访问时跳转到网页
        models.GameNews.objects.filter(pk=self.kwargs['pk']).update(views_count=F('views_count') + 1)
        return super().retrieve(request, *args, **kwargs)
