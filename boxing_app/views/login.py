from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from biz import redis_const, redis_client
from boxing_app.serializers import LoginIsNeedCaptchaSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def login_is_need_captcha(request):
    serializer = LoginIsNeedCaptchaSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    is_need = redis_client.redis_client.exists(redis_const.HAS_LOGINED.format(
        mobile=serializer.validated_data['mobile']))
    return Response({"result": is_need}, status=status.HTTP_200_OK)
