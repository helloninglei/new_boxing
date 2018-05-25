# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from boxing_app.serializers import ReportSerializer
from biz.constants import REPORT_REASON_CHOICES
from biz.utils import get_model_class_by_name


class ReportViewSet(ModelViewSet):
    serializer_class = ReportSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(dict(REPORT_REASON_CHOICES))

    def perform_create(self, serializer):
        object_class = get_model_class_by_name(self.kwargs['object_type'])
        content_object = object_class.objects.get(id=self.request.POST['object_id'])
        kwargs = {
            'user': self.request.user,
            'content_object': content_object
        }
        serializer.save(**kwargs)
