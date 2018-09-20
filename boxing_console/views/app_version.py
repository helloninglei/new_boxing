# -*- coding:utf-8 -*-
from biz.models import AppVersion
from rest_framework import viewsets, permissions
from boxing_console.serializers import AppVersionSerializer
from rest_framework.response import Response
from boxing_app.pagination import BoxingPagination


class AppVersionViewSet(viewsets.ModelViewSet):
    serializer_class = AppVersionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BoxingPagination
    queryset = AppVersion.objects.all()
