# -*- coding:utf-8 -*-
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from distutils.version import StrictVersion
from boxing_app.pagination import BoxingPagination
from boxing_console.serializers import AppVersionSerializer
from biz.models import AppVersion
from biz.constants import ANDROID, IOS, APPVERSION_FUTURE, APPVERSION_NOW, APPVERSION_PAST, VERSION_MANAGER_GROUP


class VersionReleasePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.id in VERSION_MANAGER_GROUP


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
            if serializer.validated_data['status'] != APPVERSION_FUTURE:
                return Response(data={'detail': '只能创建未发布版本'}, status=400)
            try:
                StrictVersion(serializer.validated_data['version'])
            except ValueError:
                return Response(data={'detail': '版本号格式错误 eg: x.y.z'}, status=400)

            if serializer.validated_data['platform'] == ANDROID:
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=ANDROID).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)
                if not serializer.validated_data['package']:
                    return Response(data={'detail': '软件包地址不能为空'}, status=400)
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=ANDROID)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '发布版本号不得低于当前版本'}, status=400)
                if serializer.validated_data['inner_number'] <= current.inner_number:
                    return Response(data={'detail': '内部版本号不得小于当前版本'}, status=400)

            if serializer.validated_data['platform'] == IOS:
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=IOS).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=IOS)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '发布版本号不得低于当前版本'}, status=400)

            serializer.save()
            return Response(status=201)

        return Response(status=400)

    def update(self, request, *args, **kwargs):
        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] != APPVERSION_FUTURE:
                return Response(data={'detail': '非未发布状态不可改变'}, status=400)
            try:
                StrictVersion(serializer.validated_data['version'])
            except ValueError:
                return Response(data={'detail': '版本号格式错误 eg: x.y.z'}, status=400)

            if 'id' in request.data.keys():
                release = AppVersion.objects.get(id=request.data['id'])
            else:
                return Response(data={'detail': '未指定ID'}, status=400)

            if serializer.validated_data['platform'] == ANDROID:
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=ANDROID)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '版本号不得低于当前版本'}, status=400)
                if not serializer.validated_data['package']:
                    return Response(data={'detail': '软件包地址不能为空'}, status=400)
                if serializer.validated_data['inner_number'] <= current.inner_number:
                    return Response(data={'detail': '内部版本号不得小于当前版本'}, status=400)
                release.package = serializer.validated_data['package']
                release.inner_number = serializer.validated_data['inner_number']

            if serializer.validated_data['platform'] == IOS:
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=IOS)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '发布版本号不得低于当前版本'}, status=400)
            release.version = serializer.validated_data['version']
            release.message = serializer.validated_data['message']
            release.force = serializer.validated_data['force']
            release.save()
            return Response(status=200)
        return Response(status=400)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def release_version(request):
    if request.user.id not in VERSION_MANAGER_GROUP:
        return Response(data={'detail': '此账户无版本管理权限'}, status=403)

    if 'id' in request.data.keys():
        release_id = int(request.data['id'])
        release = AppVersion.objects.get(id=release_id)
        if release.status != APPVERSION_FUTURE:
            return Response(data={'detail': '当前状态不是未发布，不可更改'}, status=400)
        current = AppVersion.objects.get(platform=release.platform, status=APPVERSION_NOW)
        current.status = APPVERSION_PAST
        release.status = APPVERSION_NOW
        current.save()
        release.save()
        return Response(status=200)
    return Response(status=400)
