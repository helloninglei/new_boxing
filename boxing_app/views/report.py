# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from biz import models
from boxing_app.serializers import ReportSerializer
from biz.constants import REPORT_OBJECT_DICT, REPORT_REASON_CHOICES


class ReportViewSet(ModelViewSet):
    serializer_class = ReportSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(REPORT_REASON_CHOICES))

    def perform_create(self, serializer):
        object_type = self.kwargs['object_type']
        object_class = getattr(models, object_type.title().replace('_', ''))
        object_class.objects.get(id=self.request.POST['object_id'])
        kwargs = {
            'user': self.request.user,
            'object_type': REPORT_OBJECT_DICT[object_type]
        }
        serializer.save(**kwargs)
