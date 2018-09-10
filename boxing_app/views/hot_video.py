# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import permission_classes, authentication_classes
from biz import models

<<<<<<< HEAD
from biz.utils import comment_count_condition, get_object_or_404
from biz.constants import PAYMENT_STATUS_PAID, HOT_VIDEO_USER_ID, HOT_VIDEO_TAG_CHOICES
from boxing_app.serializers import HotVideoSerializer
=======
from biz.utils import comment_count_condition
from biz.constants import PAYMENT_STATUS_PAID, HOT_VIDEO_USER_ID, HOT_VIDEO_TAG_CHOICES_FOR_FILTER
from boxing_app.filters import HotVideoFilter
from boxing_app.serializers import HotVideoSerializer, HotVideoDetailSerializer
>>>>>>> master_3.3.0
from boxing_app.tasks import incr_hot_video_views_count


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def hot_video_redirect(request):
    url = f'users/{HOT_VIDEO_USER_ID}/hot_videos?page={request.GET.get("page") or 1}'
    return redirect(url)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def hot_video_item_redirect(_, pk):
    user_id = get_object_or_404(models.HotVideo, pk=pk).id
    return redirect(f'/users/{user_id}/hot_videos/{pk}')


class HotVideoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HotVideoSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = HotVideoFilter

    def retrieve(self, request, *args, **kwargs):
        self.serializer_class = HotVideoDetailSerializer
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
        ).prefetch_related('users', 'users__user_profile', 'users__boxer_identification')


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def hot_video_tag_list(_):
    return Response({'result': [{'id': k, 'name': v} for k, v in HOT_VIDEO_TAG_CHOICES_FOR_FILTER]})
