# -*- coding:utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from distutils.version import StrictVersion
from boxing_app.pagination import BoxingPagination
from boxing_console.serializers import AppVersionSerializer
from biz.models import AppVersion
from biz.constants import ANDROID, IOS, APPVERSION_FUTURE, APPVERSION_NOW, APPVERSION_PAST
from boxing_console.permissions import VersionReleasePermission


class AppVersionViewSet(viewsets.ModelViewSet):
    serializer_class = AppVersionSerializer
    permission_classes = (VersionReleasePermission,)
    pagination_class = BoxingPagination
    queryset = AppVersion.objects.all()

    def retrieve(self, request, *args, **kwargs):
        return super(AppVersionViewSet, self).retrieve(request, *args, **kwargs)

    def create(self, request):
        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['platform'] == ANDROID:
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=ANDROID).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            if serializer.validated_data['platform'] == IOS:
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=IOS).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            serializer.save()
            return Response(status=201)

        return Response(status=400)

    def update(self, request, *args, **kwargs):
        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid():
            if 'id' in request.data.keys() and isinstance(request.data['id'], int):
                release = AppVersion.objects.filter(id=request.data['id']).first()
                if not release:
                    return Response(data={'detail': '版本记录不存在'}, status=400)
            else:
                return Response(data={'detail': '未指定ID'}, status=400)

            if serializer.validated_data['platform'] == ANDROID:
                android_future = AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=ANDROID).first()
                if android_future and android_future.id != release.id:
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            if serializer.validated_data['platform'] == IOS:
                ios_future = AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=IOS).first()
                if ios_future and ios_future.id != release.id:
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            release.version = serializer.validated_data['version']
            release.message = serializer.validated_data['message']
            release.force = serializer.validated_data['force']
            release.platform = serializer.validated_data['platform']
            release.inner_number = serializer.validated_data['inner_number']
            release.package = serializer.validated_data['package']
            release.save()
            return Response(status=200)
        return Response(status=400)


@api_view(['POST'])
@permission_classes([VersionReleasePermission])
def release_version(request):
    if 'id' in request.data.keys() and isinstance(request.data['id'], int):
        release = AppVersion.objects.filter(id=int(request.data['id'])).first()
        if not release:
            return Response(data={'detail': '版本记录不存在'}, status=400)
        if release.status != APPVERSION_FUTURE:
            return Response(data={'detail': '当前状态不是未发布，不可更改'}, status=400)

        current = AppVersion.objects.get(platform=release.platform, status=APPVERSION_NOW)
        current.status = APPVERSION_PAST
        release.status = APPVERSION_NOW
        current.save()
        release.save()
        return Response(status=200)
    return Response(status=400)
