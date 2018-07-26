# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from biz.utils import get_object_or_404
from biz.models import Like, Message
from boxing_app.serializers import LikeSerializer
from biz.redis_client import like_hot_video, unlike_hot_video


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
            serializer.save(user=self.request.user, message=self._get_message_instance())
        except IntegrityError as e:
            if 'Duplicate entry' not in str(e):
                raise e


class HotVideoLikeViewSet(viewsets.GenericViewSet):
    serializer_class = LikeSerializer
    queryset = object()

    def destroy(self, request, *args, **kwargs):
        unlike_hot_video(request.user.id, self.kwargs['video_id'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        like_hot_video(request.user.id, self.kwargs['video_id'])
        return Response(status=status.HTTP_201_CREATED)
