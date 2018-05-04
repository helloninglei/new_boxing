# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from biz.models import Like
from biz.models import Message
from boxing_app.serializers import LikeSerializer


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer

    def _get_message_instance(self):
        message_id = self.kwargs['message_id']
        return Message.objects.get(id=message_id)

    def get_queryset(self):
        return Like.objects.filter(message=self._get_message_instance()).prefetch_related('user')

    def destroy(self, request, *args, **kwargs):
        Like.objects.filter(user=request.user, message=self._get_message_instance()).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, message=self._get_message_instance())
