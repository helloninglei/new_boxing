# coding:utf-8
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from boxing_app.serializers import PaySerializer
from biz.services.pay_service import PayService


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_order(request, object_type):
    serializer = PaySerializer(data=request.data, context={'request': request, 'object_type': object_type})
    serializer.is_valid(raise_exception=True)
    pay_info = PayService.create_order(
        user=request.user,
        obj=serializer.data['content_object'],
        payment_type=serializer.validated_data['payment_type'],
        device=serializer.data['device'],
        ip=serializer.data['ip'])
    return Response({'pay_info': pay_info})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_unpaid_order(request, object_type):
    serializer = PaySerializer(data=request.data, context={'request': request, 'object_type': object_type})
    serializer.is_valid(raise_exception=True)
    PayService.perform_create_order(
        user=request.user,
        obj=serializer.data['content_object'],
        payment_type=serializer.validated_data.get('payment_type'),
        device=serializer.data['device'])
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def alipay_calback(request):
    return HttpResponse(PayService.on_alipay_callback(request.data))


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def wechat_calback(request):
    return HttpResponse(PayService.on_wechat_callback(request.data))
