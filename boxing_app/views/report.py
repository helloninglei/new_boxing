# -*- coding: utf-8 -*-
from biz.models import Message
from rest_framework import viewsets
from boxing_app.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        message_id = self.kwargs['message_id']
        kwargs = {
            'user': self.request.user,
            'message': Message.objects.get(id=message_id)
        }
        serializer.save(**kwargs)