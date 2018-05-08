
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from biz.services.captcha_service import get_captcha


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def captcha_image(request):
    return Response(data=get_captcha(), status=status.HTTP_200_OK)
