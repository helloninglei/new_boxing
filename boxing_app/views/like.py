# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from rest_framework import status, mixins
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from biz.utils import get_object_or_404
from biz.models import Like, Message
from biz.redis_client import like_hot_video, unlike_hot_video
from boxing_app.serializers import LikeSerializer, LikeMeListSerializer
from biz.easemob_client import EaseMobClient


class MessageLikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def _get_message_instance(self):
        return get_object_or_404(Message, id=self.kwargs['message_id'])

    def get_queryset(self):
        return Like.objects.filter(message=self._get_message_instance()).prefetch_related('user')

    def destroy(self, request, *args, **kwargs):
        Like.objects.filter(user=request.user, message=self._get_message_instance()).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        try:
            instance = serializer.save(user=self.request.user, message=self._get_message_instance())
        except IntegrityError as e:
            if 'Duplicate entry' not in str(e):
                raise e
        else:
            EaseMobClient.send_passthrough_message([instance.message.user.id])


class HotVideoLikeViewSet(views.APIView):

    def delete(self, request, *args, **kwargs):
        unlike_hot_video(request.user.id, kwargs['video_id'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        like_hot_video(request.user.id, kwargs['video_id'])
        return Response(status=status.HTTP_201_CREATED)


class LikeMeListViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeMeListSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Like.objects.filter(message__is_deleted=False, message__user=request.user.id).select_related('user', 'message')
        return super().list(request, *args, **kwargs)
