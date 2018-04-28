# -*- coding: utf-8 -*-
from biz.models import Message
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from boxing_app.serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):

    queryset = Message.objects.all().prefetch_related('user')
    serializer_class = MessageSerializer

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def hot(self, request, *args, **kwargs):  #TODO 依赖评论和点赞部分
        pass

