# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from django.shortcuts import redirect
from rest_framework import viewsets, permissions
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes, authentication_classes
from biz import models
from biz.constants import PAYMENT_STATUS_PAID, HOT_VIDEO_USER_ID
from boxing_app.serializers import HotVideoSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def hot_video_redirect(request):
    url = reverse('hot-video', kwargs={'user_id': HOT_VIDEO_USER_ID})
    return redirect(url)


class HotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotVideoSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        _filter = Q(orders__status=PAYMENT_STATUS_PAID, orders__user_id=self.request.user.id)
        pk = self.kwargs['user_id']
        return models.HotVideo.objects.filter(
            user=models.User.objects.get(pk=pk),
            is_show=True,
        ).annotate(
            is_paid=Count('orders', filter=_filter),
            comment_count=Count('comments', distinct=True),
        ).order_by('-created_time')
