# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from biz.models import Comment, Message
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from boxing_app.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission,)
    serializer_class = CommentSerializer

    def _get_message_instance(self):
        message_id = self.kwargs['message_id']
        return Message.objects.get(id=message_id)

    def get_queryset(self):
        return Comment.objects.filter(message=self._get_message_instance(), parent=None).prefetch_related('user')

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
            'message': self._get_message_instance()
        }
        serializer.save(**kwargs)

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReplyViewSet(CommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(message=self._get_message_instance()).prefetch_related('user')

    def perform_create(self, serializer):
        obj = self.get_object()
        kwargs = {
            'user': self.request.user,
            'message': self._get_message_instance(),
            'parent': obj,
            'ancestor_id': obj.ancestor_id or obj.id,
        }
        serializer.save(**kwargs)