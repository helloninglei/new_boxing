import requests
from django.urls import reverse
# from django
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from django.contrib.auth import authenticate, login as user_login, logout
from boxing_app.serializers import LoginSerializer
from biz import redis_const, redis_client


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    credentials = dict(username=serializer.validated_data['mobile'], password=serializer.validated_data['password'])

    user = authenticate(**credentials)
    redis_client.setex(redis_const.HAS_LOGINED.format(mobile=serializer.validated_data['mobile']), 60, "1")
    if not user:
        return Response({"message": "用户名或密码错误"}, status=status.HTTP_400_BAD_REQUEST)

    return Response(user_login(request, user), status=status.HTTP_200_OK)

    # print(reverse("rest_login"))
    # response = requests.post(reverse("rest_login"), data={
    #     "username": serializer.validated_data['mobile'], "password": serializer.validated_data['password']})
    # if response.status_code == status.HTTP_400_BAD_REQUEST:
    #     return Response({"message": "密码错误!"}, status.HTTP_400_BAD_REQUEST)
    # return response


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def login_is_need_captcha(request):
    is_need = redis_client.exists(redis_const.HAS_LOGINED.format(mobile=request.query_params.get("mobile")))
    return Response({"result": is_need}, status=status.HTTP_200_OK)
