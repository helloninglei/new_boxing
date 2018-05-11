# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from django.db.models import Count, Sum
from biz import models
from boxing_console.serializers import HotVideoSerializer
from boxing_console.filters import HotVideoFilter, CommonFilter


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = HotVideoFilter
    search_fields = ('user__id', 'name')

    def get_queryset(self):
        return models.HotVideo.objects.annotate(sales_count=Count('orders'), price_amount=Sum('orders__amount')).\
            all().order_by('-created_time').prefetch_related('orders')
