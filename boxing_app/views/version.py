from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from biz.utils import get_device_platform
from biz.constants import DEVICE_PLATFORM
from biz.models import AppVersion
from biz.constants import APPVERSION_NOW, ANDROID, IOS

platform_mapping = {
    'ANDROID': ANDROID,
    'IOS': IOS
}


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def version(request):
    device = dict(DEVICE_PLATFORM).get(get_device_platform(request))
    if device:
        current = AppVersion.objects.get(platform=platform_mapping.get(device.upper()), status=APPVERSION_NOW)
        version_response = {'version': current.version, 'message': current.message, 'force': current.force}
        if platform_mapping.get(device.upper()) == ANDROID:
            version_response['version_code'] = current.inner_number
            version_response['url'] = current.package
        return Response(data=version_response, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
