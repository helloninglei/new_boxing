# -*- coding: utf-8 -*-
import json
from biz.models import Message
from rest_framework import viewsets, status
from rest_framework.response import Response
from boxing_app.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user == obj.user:
            obj.is_deleted = True
            obj.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def hot(self, request, *args, **kwargs):
        pass

