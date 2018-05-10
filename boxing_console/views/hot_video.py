# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status

from django.db.models import Count, Sum
from biz import models
from boxing_console.serializers import HotVideoSerializer


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    # filter_fields = ('created_time',)
    search_fields = ('user__id', 'name', 'description')

    def get_queryset(self):
        return models.HotVideo.objects.annotate(sales_count=Count('orders'), price_amount=Sum('orders__amount')).\
            all().order_by('-created_time').prefetch_related('orders')
