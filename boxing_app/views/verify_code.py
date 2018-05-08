"""
验证码：
不用业务场景可能有不同的短信验证码发送规则，可以使用不同view来处理，但不同的view均需加入短信接口的保护措施。
如果其他业务场景可以复用view，需要将业务场景加入doc。
"""
import random
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from biz import redis_client
from boxing_app.serializers import SendVerifyCodeSerializer
from biz import ali_sms_client
from biz.redis_const import SEND_VERIFY_CODE, SEND_VERIFY_INTERVAL


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_verify_code(request):
    """
    注册业务、
    """
    serializer = SendVerifyCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    verify_code = random.randint(100000, 999999)
    redis_client.setex(SEND_VERIFY_CODE.format(mobile=serializer.validated_data['mobile']), SEND_VERIFY_INTERVAL,
                       verify_code)
    ali_sms_client.send_verify_code(serializer.validated_data['mobile'], verify_code)
    return Response(status=status.HTTP_200_OK)
