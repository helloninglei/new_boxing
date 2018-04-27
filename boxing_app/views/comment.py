# -*- coding: utf-8 -*-
from biz.models import Comment, Message
from rest_framework import viewsets, status
from rest_framework.response import Response
from boxing_app.serializers import CommentSerializer, ReplySerializer
from django.db import transaction


class CommentViewSet(viewsets.ModelViewSet):
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
        super(CommentViewSet, self).destroy()
        obj = self.get_object()
        if request.user == obj.user:
            with transaction.atomic():
                obj.is_deleted = True
                obj.save()
                Comment.objects.filter(parent_id=obj.id).update(is_deleted=True)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class ReplyViewSet(CommentViewSet):
    serializer_class = ReplySerializer

    def get_queryset(self):
        return Comment.objects.filter(message=self._get_message_instance()).prefetch_related('user')

    def perform_create(self, serializer):
        obj = self.get_object()
        print(obj)
        kwargs = {
            'user': self.request.user,
            'message': self._get_message_instance(),
            'parent': obj
        }
        parent = obj.parent
        if parent:
            if parent.parent:
                ancestor_id = parent.ancestor_id
            else:
                ancestor_id = obj.parent.id
        else:
            ancestor_id = obj.id

        kwargs['ancestor_id'] = ancestor_id
        serializer.save(**kwargs)