# -*- coding: utf-8 -*-
from django_filters import rest_framework as df_filters
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum, Q
from django.contrib.contenttypes.fields import ContentType
from biz import models
from biz.constants import PAYMENT_STATUS_PAID, PAYMENT_STATUS_UNPAID
from boxing_console.serializers import HotVideoSerializer, HotVideoShowSerializer, HotVideoUserSerializer
from boxing_console.filters import HotVideoFilter


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = HotVideoFilter

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
        ).prefetch_related('users', 'users__user_profile').order_by('-created_time')

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = HotVideoShowSerializer
        return super().partial_update(request, *args, **kwargs)


@api_view(['GET'])
def hot_video_user_list(_):
    serializer = HotVideoUserSerializer(models.User.objects.filter(user_type__isnull=False), many=True)
    return Response(serializer.data)
