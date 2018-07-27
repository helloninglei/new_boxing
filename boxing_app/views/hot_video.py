# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from django.shortcuts import redirect
from rest_framework.reverse import reverse
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes, authentication_classes
from biz import models

from biz.utils import comment_count_condition
from biz.constants import PAYMENT_STATUS_PAID, HOT_VIDEO_USER_ID
from boxing_app.serializers import HotVideoSerializer
from boxing_app.tasks import incr_hot_video_views_count
from boxing_app.filters import HotVideoFilter


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def hot_video_redirect(_):
    url = reverse('hot-video', kwargs={'user_id': HOT_VIDEO_USER_ID})
    return redirect(url)


class HotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotVideoSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = HotVideoFilter

    def retrieve(self, request, *args, **kwargs):
        print(kwargs)
        video_id = kwargs['pk']
        incr_hot_video_views_count.delay(video_id)
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_PAID, orders__user_id=self.request.user.id)
        pk = self.kwargs['user_id']
        return models.HotVideo.objects.filter(
            users__in=[pk],
            is_show=True,
        ).annotate(
            is_paid=Count('orders', filter=_filter),
            comment_count=comment_count_condition,
        ).prefetch_related('users', 'users__user_profile')
