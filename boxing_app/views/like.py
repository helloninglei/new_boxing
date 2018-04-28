# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from biz.models import Like
from biz.models import Message
from boxing_app.serializers import LikeSerializer
from boxing_app.permissions import OnlyOwnerCanDeletePermission

class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission,)
    serializer_class = LikeSerializer

    def _get_message_instance(self):
        message_id = self.kwargs['message_id']
        return Message.objects.get(id=message_id)

    def get_queryset(self):
        print(self._get_message_instance())
        return Like.objects.filter(message=self._get_message_instance()).prefetch_related('user')

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        self.check_object_permissions(request, obj)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, message=self._get_message_instance())
