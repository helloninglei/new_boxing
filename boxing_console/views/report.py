# -*- coding: utf-8 -*-
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters import rest_framework as df_filters
from biz import models
from boxing_console.filters import ReportFilter
from boxing_console.serializers import ReportSerializer, ReportHandleSerializer
from biz.constants import REPORT_STATUS_DELETED, REPORT_STATUS_PROVED_FALSE, REPORT_STATUS_NOT_PROCESSED


class ReportViewSet(ModelViewSet):
    serializer_class = ReportSerializer
    filter_backends = (df_filters.DjangoFilterBackend,)
    filter_class = ReportFilter

    def get_queryset(self):
        return models.Report.objects.all().prefetch_related('user', 'content_object',
                                                            'content_object__user')


class ReportHandleViewSet(ModelViewSet):
    serializer_class = ReportHandleSerializer
    queryset = models.Report.objects.all()

    def _get_object(self):
        return models.Report.objects.filter(pk=self.get_object().pk, status=REPORT_STATUS_NOT_PROCESSED)

    def proved_false(self, request, *args, **kwargs):
        self._get_object().update(status=REPORT_STATUS_PROVED_FALSE)
        return Response(status=status.HTTP_200_OK)

    def do_delete(self, request, *args, **kwargs):
        self._get_object().update(status=REPORT_STATUS_DELETED)
        obj = self.get_object().content_object
        if hasattr(obj, 'is_deleted'):
            obj.soft_delete()
        else:
            obj.delete()
        return Response(status=status.HTTP_200_OK)
