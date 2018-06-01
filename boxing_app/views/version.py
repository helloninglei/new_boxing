from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from django.conf import settings
from biz.utils import get_device_platform
from biz.constants import DEVICE_PLATFORM

version_mapping = {
    'ANDROID': settings.ANDROID_VERSION,
    'IOS': settings.IOS_VERSION,
}


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def version(request):
    device = dict(DEVICE_PLATFORM).get(get_device_platform(request))
    if device is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    version_response = version_mapping.get(device.upper())
    if version_response:
        return Response(version_response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)
