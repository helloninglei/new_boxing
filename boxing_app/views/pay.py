# coding:utf-8
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.response import Response
from boxing_app.serializers import PaySerializer
from biz.services.pay_service import PayService
from biz.parser import XMLParser


@api_view(['POST'])
def create_order(request, object_type):
    serializer = PaySerializer(data=request.data, context={'request': request, 'object_type': object_type})
    serializer.is_valid(raise_exception=True)
    pay_info = PayService.create_order(
        user=request.user,
        obj=serializer.data['content_object'],
        payment_type=serializer.validated_data['payment_type'],
        device=serializer.data['device'],
        ip=serializer.data['ip'])
    return Response(pay_info)


@api_view(['POST'])
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
@parser_classes((XMLParser,))
def wechat_calback(request):
    return HttpResponse(PayService.on_wechat_callback(request.data))


@api_view(['GET'])
def pay_status(request):
    order_id = request.query_params.get('order_id')
    info = PayService.get_payment_status_info(order_id, request.user)
    if info:
        if info['status'] == 'paid':
            return Response({'result': info})
        return Response(data={'message': ['支付失败了，请稍后重试']}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': '订单不存在'}, status=status.HTTP_404_NOT_FOUND)
