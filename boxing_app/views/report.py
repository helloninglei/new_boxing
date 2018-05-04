# -*- coding: utf-8 -*-
from biz import models
from rest_framework import viewsets
from biz.models import Message
from boxing_app.serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    serializer_class = ReportSerializer
    queryset = models.Report.objects.all()

    def perform_create(self, serializer):
        object_type = self.kwargs['object_type']
        object_id = self.kwargs['object_id']
        object_class = getattr(models, object_type.title())
        print(object_class.objects.get(id=id))
        message_id = self.kwargs['message_id']
        kwargs = {
            'user': self.request.user,
            'message': Message.objects.get(id=message_id)
        }
        serializer.save(**kwargs)