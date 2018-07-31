# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from rest_framework import status, mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from biz.utils import get_object_or_404
from biz.models import Like, Message
from boxing_app.serializers import LikeSerializer, LikeMeListSerializer


class LikeViewSet(viewsets.ModelViewSet):
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


class LikeMeListViewSet(mixins.ListModelMixin,
                        GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeMeListSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = Like.objects.filter(message__user=request.user.id).select_related('user', 'message')
        return super().list(request, *args, **kwargs)
