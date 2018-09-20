# -*- coding:utf-8 -*-
from biz.models import AppVersion
from rest_framework import viewsets, permissions
from boxing_console.serializers import AppVersionSerializer
from rest_framework.response import Response
from boxing_app.pagination import BoxingPagination
from biz.constants import APPVERSION_FUTURE


class AppVersionViewSet(viewsets.ModelViewSet):
    serializer_class = AppVersionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BoxingPagination
    queryset = AppVersion.objects.all()

    def create(self, request):
        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid():
            #  只能创建未发布版本
            if serializer.validated_data['status'] != APPVERSION_FUTURE:
                return Response(status=400)

            serializer.save()
            return Response(status=201)
        return Response(status=400)
