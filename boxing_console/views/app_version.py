# -*- coding:utf-8 -*-
from biz.models import AppVersion
from rest_framework import viewsets, permissions
from boxing_console.serializers import AppVersionSerializer
from rest_framework.response import Response
from boxing_app.pagination import BoxingPagination
from biz.constants import APPVERSION_FUTURE, ANDROID, IOS, APPVERSION_NOW, VERSION_MANAGERS
from distutils.version import StrictVersion


class AppVersionViewSet(viewsets.ModelViewSet):
    serializer_class = AppVersionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = BoxingPagination
    queryset = AppVersion.objects.all()

    def create(self, request):
        if request.user.id not in VERSION_MANAGERS:
            return Response(data={'detail': '此账户无版本管理权限'}, status=403)

        serializer = AppVersionSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['status'] != APPVERSION_FUTURE:
                return Response(data={'detail': '只能创建未发布版本'}, status=400)
            try:
                StrictVersion(serializer.validated_data['version'])
            except ValueError:
                return Response(data={'detail': '版本号格式错误 eg: x.y.z'}, status=400)

            if serializer.validated_data['platform'] == ANDROID:
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=ANDROID)
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=ANDROID).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '发布版本号不得低于当前版本'}, status=400)
                if not serializer.validated_data['package']:
                    return Response(data={'detail': '软件包地址不能为空'}, status=400)
                if serializer.validated_data['inner_number'] <= current.inner_number:
                    return Response(data={'detail': '内部版本号不得小于当前版本'}, status=400)

            if serializer.validated_data['platform'] == IOS:
                current = AppVersion.objects.get(status=APPVERSION_NOW, platform=IOS)
                if AppVersion.objects.filter(status=APPVERSION_FUTURE, platform=IOS).exists():
                    return Response(data={'detail': '当前平台已有一个未发布版本'}, status=400)
                if StrictVersion(serializer.validated_data['version']) <= StrictVersion(current.version):
                    return Response(data={'detail': '发布版本号不得低于当前版本'}, status=400)

            serializer.save()
            return Response(status=201)

        return Response(status=400)
