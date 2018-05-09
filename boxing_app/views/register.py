from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from biz.models import User, UserProfile
from biz import redis_client, redis_const
from boxing_app.serializers import RegisterSerializer, RegisterWithInfoSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def mobile_register_status(request):
    mobile = request.query_params.get("mobile")
    is_exists = User.objects.filter(mobile=mobile).exists()
    return Response(data={"result": is_exists}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def is_need_captcha(request):
    mobile = request.query_params.get("mobile")
    is_need = redis_client.exists(redis_const.SENDING_VERIFY_CODE.format(mobile=mobile))
    return Response(data={'result': is_need}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile = serializer.validated_data['mobile']
    password = serializer.validated_data['password']
    redis_client.hmset(
        redis_const.REGISTER_INFO.format(mobile=mobile), {"mobile": mobile, "password": password})
    return Response(data={"result": "ok"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_with_user_info(request):
    serializer = RegisterWithInfoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mobile, password = redis_client.hmget(
        redis_const.REGISTER_INFO.format(mobile=(serializer.validated_data['mobile'])), ["mobile", "password"])
    user = User.objects.create_user(mobile=mobile, password=password)
    UserProfile.objects.create(user=user, gender=serializer.validated_data['gender'],
                               avatar=serializer.validated_data['avatar'])
    return Response(data={"result": "ok"}, status=status.HTTP_204_NO_CONTENT)
