from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from biz.models import User, UserProfile
from biz import redis_client, redis_const
from boxing_app.serializers import RegisterSerializer, RegisterWithInfoSerializer, ChangeMobileSerializer
from boxing_app.tasks import register_easemob_account, send_message
from biz.redis_client import follow_user
from biz.constants import SERVICE_USER_ID
from biz.utils import hans_to_initial


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
    is_need = redis_client.redis_client.exists(redis_const.SENDING_VERIFY_CODE.format(mobile=mobile))
    return Response(data={'result': is_need}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    mobile = serializer.validated_data['mobile']
    password = serializer.validated_data['password']
    wechat_openid = serializer.validated_data.get("wechat_openid")
    weibo_openid = serializer.validated_data.get("weibo_openid")
    register_data = {"mobile": mobile, "password": password, "wechat_openid": wechat_openid,
                     "weibo_openid": weibo_openid}
    register_data = {k: v for k, v in register_data.items() if v}
    redis_client.redis_client.hmset(
        redis_const.REGISTER_INFO.format(mobile=mobile), register_data)
    return Response(data={"result": "ok"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_with_user_info(request):
    serializer = RegisterWithInfoSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    mobile, password, wechat_openid, weibo_openid = redis_client.redis_client.hmget(
        redis_const.REGISTER_INFO.format(mobile=(serializer.validated_data['mobile'])),
        ["mobile", "password", "wechat_openid", "weibo_openid"])
    user = User.objects.create_user(
        mobile=mobile, password=password, wechat_openid=wechat_openid, weibo_openid=weibo_openid)
    follow_user(user.id, SERVICE_USER_ID)
    send_message.delay(user.id)
    UserProfile.objects.filter(user=user).update(gender=serializer.validated_data['gender'],
                                                 avatar=serializer.validated_data['avatar'],
                                                 nick_name=serializer.validated_data['nick_name'],
                                                 nick_name_index_letter=hans_to_initial(
                                                     serializer.validated_data['nick_name']))
    register_easemob_account.delay(user.id)
    redis_client.redis_client.delete(redis_const.REGISTER_INFO.format(mobile=serializer.validated_data['mobile']))
    return Response(data={"result": "ok"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def change_mobile(request):
    serializer = ChangeMobileSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    User.objects.filter(id=request.user.id).update(mobile=serializer.validated_data['mobile'])
    return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
