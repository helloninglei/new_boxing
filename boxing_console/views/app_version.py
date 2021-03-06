# -*- coding:utf-8 -*-
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from boxing_console.serializers import AppVersionSerializer
from biz.models import AppVersion
from biz.constants import ANDROID, IOS, APPVERSION_FUTURE, APPVERSION_NOW, APPVERSION_PAST
from boxing_console.permissions import VersionReleasePermission


class AppVersionViewSet(viewsets.ModelViewSet):
    serializer_class = AppVersionSerializer
    permission_classes = (VersionReleasePermission,)
    queryset = AppVersion.objects.all()

    def create(self, request):
        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
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
            release = AppVersion.objects.filter(id=kwargs['pk']).first()
            if not release:
                return Response(data={'detail': '版本记录不存在'}, status=404)

            if serializer.validated_data['platform'] == ANDROID:
                android_future = AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=ANDROID).first()
                if android_future and android_future.id != release.id:
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            if serializer.validated_data['platform'] == IOS:
                ios_future = AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=IOS).first()
                if ios_future and ios_future.id != release.id:
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)

            super().update(request, *args, **kwargs)
            return Response(status=200)
        return Response(status=400)


@api_view(['POST'])
@permission_classes([VersionReleasePermission])
def release_version(request, pk):
    release = AppVersion.objects.filter(id=pk).first()
    if not release:
        return Response(data={'detail': '版本记录不存在'}, status=404)
    if release.status != APPVERSION_FUTURE:
        return Response(data={'detail': '版本记录状态不是未发布'}, status=400)

    current = AppVersion.objects.get(platform=release.platform, status=APPVERSION_NOW)
    current.status = APPVERSION_PAST
    release.status = APPVERSION_NOW
    current.save()
    release.save()
    return Response(status=200)
