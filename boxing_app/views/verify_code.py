
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status
from rest_framework.response import Response
from boxing_app.serializers import SendVerifyCodeSerializer
from biz import sms_client


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def send_verify_code(request):
    """
    注册
    """
    serializer = SendVerifyCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    sms_client.send_verify_code(serializer.validated_data['mobile'])
    return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
