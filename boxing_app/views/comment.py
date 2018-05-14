# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from biz import models
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from boxing_app.serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission,)
    serializer_class = CommentSerializer

    @property
    def object_type(self):
        return getattr(models, self.kwargs['object_type'].title().replace('_', ''))

    @property
    def object_id(self):
        return self.kwargs['object_id']

    @property
    def content_object(self):
        return self.object_type.objects.get(pk=self.object_id)

    def get_queryset(self):
        return self.content_object.comments.filter(parent=None).prefetch_related('user')

    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
            'content_object': self.content_object,
        }
        serializer.save(**kwargs)


class ReplyViewSet(CommentViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(pk=self.kwargs['pk'])

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        obj = self.get_object()
        kwargs = {
            'user': self.request.user,
            'content_object': self.content_object,
            'parent': obj,
            'ancestor_id': obj.ancestor_id or obj.id,
        }
        serializer.save(**kwargs)
