
from rest_framework import mixins, viewsets
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from biz.models import User
from boxing_app.serializers import RegisterSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def mobile_is_exist(request):
    pass


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    mobile = request.data.get("mobile")
    if User.objects.filter(mobile=mobile).exists():
        return Response(response_message_format("手机号已存在!"), status.HTTP_400_BAD_REQUEST)


class RegisterViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer
    queryset = User.objects.all()

    def mobile_is_register(self, request):
        mobile_register_status = self.queryset.filter(mobile=request.data.get('mobile')).exists()
        return Response({"result": mobile_register_status}, status=status.HTTP_200_OK)

    def register_account(self, request):
        # todo, 校验短信验证码。
        serializer = self.get_serializer()
        # redis 存注册的手机号和密码。

        return Response(status=status.HTTP_204_NO_CONTENT)

    def register(self, request):
        # 根据手机号，从redis取之前存入的手机号和密码。
        # 校验传入的个人资料。
        # 存入用户，存入个人资料。
        pass
