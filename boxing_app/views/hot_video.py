# -*- coding: utf-8 -*-
from rest_framework import viewsets
from django.db.models import Count, Q
from biz import models
from biz.constants import PAYMENT_STATUS_PAID
from boxing_app.serializers import HotVideoSerializer


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_PAID, user=self.request.user)
        pk = self.kwargs['user_id']
        return models.HotVideo.objects.filter(
            user=models.User.objects.get(pk=pk),
            is_show=True,
        ).annotate(
            is_paid=Count('orders', filter=_filter),
            comment_count=Count('comments'),
        ).order_by('-created_time')
