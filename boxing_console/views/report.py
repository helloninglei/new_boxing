# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db.transaction import atomic
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view
from rest_framework import filters
from django_filters import rest_framework as df_filters
from biz import models
from boxing_console.filters import ReportFilter
from boxing_console.serializers import ReportSerializer
from biz.constants import REPORT_STATUS_DELETED, REPORT_STATUS_PROVED_FALSE, REPORT_STATUS_NOT_PROCESSED


class ReportViewSet(ModelViewSet):
    serializer_class = ReportSerializer
    filter_backends = (df_filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = ReportFilter
    search_fields = ('user__id', )

    def get_queryset(self):
        return models.Report.objects.all().prefetch_related('user', 'content_object',
                                                            'content_object__user__user_profile', 'operator__user_profile')


def _get_object(pk):
    return models.Report.objects.filter(pk=pk, status=REPORT_STATUS_NOT_PROCESSED)


@api_view(['POST'])
def proved_false(request, pk):
    _get_object(pk).update(status=REPORT_STATUS_PROVED_FALSE, operator=request.user, updated_time=timezone.now())
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@atomic
def do_delete(request, pk):
    report_obj = _get_object(pk)
    obj = report_obj.first().content_object
    report_obj.update(status=REPORT_STATUS_DELETED, operator=request.user, updated_time=timezone.now())
    if hasattr(obj, 'is_deleted'):
        obj.soft_delete()
    elif hasattr(obj, 'is_show'):
        obj.is_show = False
        obj.save()
    else:
        raise Exception('can not delete')  # 不支持软删除的model无法处理
    return Response(status=status.HTTP_200_OK)
