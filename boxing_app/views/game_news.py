# -*- coding: utf-8 -*-
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, authentication_classes
from django.db.models import F
from biz import models
from biz.utils import comment_count_condition
from boxing_app import serializers

h5_base_url = settings.SHARE_H5_BASE_URL


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])
def get_news_url(request, pk):
    return Response({'url': f'{h5_base_url}game_news/{pk}/1'})  # 1 在app内打开


class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.NewsSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()
    queryset = models.GameNews.objects.filter(is_show=True).annotate(comment_count=comment_count_condition)

    def retrieve(self, request, *args, **kwargs):
        news_id = self.kwargs['pk']
        models.GameNews.objects.filter(pk=news_id).update(views_count=F('views_count') + 1)
        return super().retrieve(request, *args, **kwargs)

    def search_news(self, request, *args, **kwargs):
        keywords = self.request.query_params.get('keywords', "")
        self.queryset = self.queryset.filter(title__icontains=keywords) if keywords else []
        return super().list(request, *args, **kwargs)
