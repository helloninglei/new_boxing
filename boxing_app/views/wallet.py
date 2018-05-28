from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from biz.models import MoneyChangeLog
from biz.models import WithdrawLog
from boxing_app.serializers import MoneyChangeLogReadOnlySerializer, RechargeSerializer, WithdrawSerializer
from boxing_app.filters import MoneyChangeLogFilter
from biz.services.pay_service import PayService
from biz.constants import PAYMENT_TYPE_ALIPAY, PAYMENT_TYPE_WECHAT
from biz.utils import get_client_ip, get_device_platform
from biz import constants


@api_view(['GET'])
def money_balance(request):
    return Response({"result": request.user.money_balance}, status=status.HTTP_200_OK)


class MoneyChangeLogViewSet(mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    serializer_class = MoneyChangeLogReadOnlySerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MoneyChangeLogFilter

    def get_queryset(self):
        return MoneyChangeLog.objects.filter(user=self.request.user).order_by('-created_time')


class WithdrawViewSet(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      viewsets.GenericViewSet):
    serializer_class = WithdrawSerializer

    def get_queryset(self):
        return WithdrawLog.objects.filter(user=self.request.user).order_by("-created_time")


@api_view(['POST'])
def recharge(request, payment_type):
    payment_dict = {"alipay": PAYMENT_TYPE_ALIPAY, "wechat": PAYMENT_TYPE_WECHAT}
    serializer = RechargeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    pay_info = PayService.create_order(
        request.user,
        request.user,
        payment_dict[payment_type],
        get_device_platform(request),
        get_client_ip(request),
        amount=serializer.validated_data['amount'],
    )
    return Response({"result": pay_info}, status=status.HTTP_200_OK)


class RechargeLogViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = MoneyChangeLogReadOnlySerializer

    def get_queryset(self):
        return MoneyChangeLog.objects.filter(
            user=self.request.user, change_type=constants.MONEY_CHANGE_TYPE_INCREASE_RECHARGE).order_by('-created_time')
