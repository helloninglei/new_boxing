# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from django.db.models import Count, Sum, Q
from biz import models
from biz.constants import PAYMENT_STATUS_WAIT_USE
from boxing_console.serializers import HotVideoSerializer
from boxing_console.filters import HotVideoFilter


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = HotVideoFilter
    search_fields = ('user__id', 'name')

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_WAIT_USE)
        return models.HotVideo.objects.annotate(
            sales_count=Count('orders', filter=_filter),
            price_amount=Sum('orders__amount', filter=_filter)
        ).order_by('-created_time')
