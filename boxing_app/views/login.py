from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from boxing_app.serializers import AuthTokenLoginSerializer
from biz import redis_const, redis_client


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def login_is_need_captcha(request):
    is_need = redis_client.redis_client.exists(redis_const.HAS_LOGINED.format(mobile=request.query_params.get("mobile")))
    return Response({"result": is_need}, status=status.HTTP_200_OK)


class AuthTokenLogin(ObtainAuthToken):
    serializer_class = AuthTokenLoginSerializer
