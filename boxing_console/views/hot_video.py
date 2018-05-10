# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Count, Sum
from biz import models
from boxing_console.serializers import HotVideoSerializer


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer

    def get_queryset(self):
        return models.HotVideo.objects.annotate(sales_count=Count('orders'), price_amount=Sum('orders__amount')).\
            all().order_by('-created_time').prefetch_related('orders')
