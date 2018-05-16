# -*- coding: utf-8 -*-
from rest_framework import viewsets, permissions
from rest_framework.reverse import reverse
from django.db.models import Count, Q
from django.shortcuts import redirect
from biz import models
from biz.constants import PAYMENT_STATUS_PAID, HOT_VIDEO_USER_ID
from boxing_app.serializers import HotVideoSerializer


def hot_videos_redirect(request):
    url = reverse('hot-video', kwargs={'user_id': HOT_VIDEO_USER_ID})
    return redirect(url)


class HotVideoViewSet(viewsets.ModelViewSet):
    serializer_class = HotVideoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_PAID, user_id=self.request.user.id)
        pk = self.kwargs['user_id']
        return models.HotVideo.objects.filter(
            user=models.User.objects.get(pk=pk),
            is_show=True,
        ).annotate(
            is_paid=Count('orders', filter=_filter),
            comment_count=Count('comments'),
        ).order_by('-created_time')


