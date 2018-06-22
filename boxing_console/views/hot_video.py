# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from django.db.models import Count, Sum, Q
from django.contrib.contenttypes.fields import ContentType
from biz import models
from biz.constants import PAYMENT_STATUS_PAID, PAYMENT_STATUS_UNPAID
from boxing_console.serializers import HotVideoSerializer, HotVideoShowSerializer
from boxing_console.filters import HotVideoFilter


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = HotVideoFilter
    search_fields = ('user__id', 'name')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        count_info = models.PayOrder.objects.filter(
            content_type=ContentType.objects.get(app_label="biz", model="hotvideo"),
            status__gt=PAYMENT_STATUS_UNPAID).aggregate(total_count=Count("id"),
                                                        total_amount=Sum("amount"))
        response.data.update(count_info)
        return response

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_PAID)
        return models.HotVideo.objects.annotate(
            sales_count=Count('orders', filter=_filter, distinct=True),
            price_amount=Sum('orders__amount', filter=_filter, distinct=True)
        ).order_by('-created_time')

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = HotVideoShowSerializer
        return super().partial_update(request, *args, **kwargs)
