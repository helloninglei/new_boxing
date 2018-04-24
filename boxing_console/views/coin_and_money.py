# -*- coding: utf-8 -*-
from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from biz import constants
from biz.models import CoinChangeLog, User
from biz.services.coin_money_handle import coin_handle, money_handle, write_coin_and_money_log_remarks
from boxing_console.filters import CoinChangLogListFilter
from boxing_console.serializers import CoinLogListSerializer


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_or_subtract_user_coin(request, effect_user_id):
    change_amount = request.data.get('change_amount')
    change_type = request.data.get('change_type')
    effect_user = User.objects.filter(pk=effect_user_id).first()
    operator = request.user.pk
    remarks = write_coin_and_money_log_remarks(request)

    if not effect_user:
        return Response({'message': u'您操作的用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
    if not change_amount:
        return Response({'message': u'请输入需要增加或减少的拳豆值'}, status=status.HTTP_400_BAD_REQUEST)
    if change_type not in dict(constants.COIN_CHANGE_TYPE_CHOICES).keys():
        return Response({'message': u'拳豆变动类型未知'}, status=status.HTTP_400_BAD_REQUEST)

    coin_change_log = coin_handle(effect_user, operator, change_amount, change_type, remarks)
    success_message = u'操作成功，用户{0}拳豆增加{1},目前拳豆余额为{2}'.format(effect_user.username,
                                                             coin_change_log.changeAmount,
                                                             coin_change_log.remainAmount)

    return Response({'message': success_message}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_or_subtract_user_money(request, effect_user_id):
    change_amount = request.data.get('change_amount')
    change_type = request.data.get('change_type')
    effect_user = User.objects.filter(pk=effect_user_id).first()
    operator = request.user.pk
    remarks = write_coin_and_money_log_remarks(request)

    if not effect_user:
        return Response({'message': u'您操作的用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
    if not change_amount:
        return Response({'message': u'请输入需要增加或减少的钱包金额'}, status=status.HTTP_400_BAD_REQUEST)
    if change_type not in dict(constants.MONEY_CHANGE_TYPE_CHOICES).keys():
        return Response({'message': u'钱包金额变动类型未知'}, status=status.HTTP_400_BAD_REQUEST)

    money_change_log = money_handle(effect_user, operator, change_amount, change_type, remarks)
    success_message = u'操作成功，用户{0}钱包金额增加{1},目前钱包余额为{2}'.format(effect_user.username,
                                                               money_change_log.changeAmount,
                                                               money_change_log.remainAmount)

    return Response({'message': success_message}, status=status.HTTP_200_OK)


class CoinChangLogViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CoinLogListSerializer
    filter_class = CoinChangLogListFilter
    queryset = CoinChangeLog.objects.filter().order_by(*['-created_time', '-id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=request.user))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return Response(self.get_paginated_response(serializer.data).data)