# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions
from django.db.models import Count, Q
from biz import models
from biz.constants import PAYMENT_STATUS_WAIT_USE
from boxing_app.serializers import HotVideoSerializer


class HotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotVideoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_WAIT_USE, user_id=self.request.user.id)
        pk = self.kwargs['user_id']
        return models.HotVideo.objects.filter(
            user=models.User.objects.get(pk=pk),
            is_show=True,
        ).annotate(
            is_paid=Count('orders', filter=_filter),
            comment_count=Count('comments'),
        ).order_by('-created_time')
