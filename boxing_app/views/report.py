# -*- coding: utf-8 -*-
from biz import models
from rest_framework.viewsets import mixins, GenericViewSet
from boxing_app.serializers import ReportSerializer
from biz.constants import REPORT_OBJECT_DICT


class ReportViewSet(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = ReportSerializer

    def perform_create(self, serializer):
        object_type = self.kwargs['object_type']
        object_class = getattr(models, object_type.title())
        object_class.objects.get(id=self.request.POST['object_id'])
        kwargs = {
            'user': self.request.user,
            'object_type': REPORT_OBJECT_DICT[object_type]
        }
        serializer.save(**kwargs)