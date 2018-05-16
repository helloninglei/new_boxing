# coding:utf-8
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from boxing_app.serializers import PaySerializer
from biz.services.pay_service import PayService


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_order(request):
    serializer = PaySerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)
    try:
        pay_info = PayService.create_order(
            user=request.user,
            obj=serializer.data['content_object'],
            payment_type=serializer.validated_data['payment_type'],
            amount=serializer.validated_data['amount'],
            device=serializer.data['device'],
        )
        return Response(pay_info)
    except ValidationError as ex:
        return Response({'message': ex.detail}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def alipay_calback(request):
    return HttpResponse(PayService.on_alipay_callback(request.data))


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def wechat_calback(request):
    return HttpResponse(PayService.on_wechat_callback(request.data))
