# -*- coding: utf-8 -*-

from biz.models import Message
from rest_framework import viewsets
from boxing_app.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
