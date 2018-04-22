# -*- coding: utf-8 -*-
from rest_framework import mixins, status
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from biz.models import CoinChangeLog, User
from biz.services.coin_money_handle import coin_handle, money_handle
from boxing_console.filters import CoinChangLogListFilter
from boxing_console.serializers import CoinLogListSerializer


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def add_or_subtract_user_coin(request, effect_user_id):
    if not request.data.get('change_amount'):
        return Response({'message': u'请输入需要增加或减少的拳豆值'}, status=status.HTTP_400_BAD_REQUEST)

    effect_user = User.objects.filter(pk=effect_user_id).first()
    if not effect_user:
        return Response({'message': u'您操作的用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        operator = request.user
        change_amount = request.data.get('change_amount', 0)
        change_reason = request.data.get('change_reason', '')
        coin_change_log = coin_handle(effect_user, operator, change_amount, change_reason)
        success_message = u'操作成功，用户{0}拳豆增加{1},目前拳豆余额为{2}'.format(effect_user.username,
                                                                 coin_change_log.changeAmount,
                                                                 coin_change_log.remainAmount)

        return Response({'message': success_message}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def add_or_subtract_user_money(request, effect_user_id):
    if not request.data.get('change_amount'):
        return Response({'message': u'请输入需要增加或减少的金额'}, status=status.HTTP_400_BAD_REQUEST)

    effect_user = User.objects.filter(pk=effect_user_id).first()
    if not effect_user:
        return Response({'message': u'您操作的用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        operator = request.user
        change_amount = request.data.get('change_amount', 0)
        change_reason = request.data.get('change_reason', '')
        money_change_log = money_handle(effect_user, operator, change_amount, change_reason)
        success_message = u'操作成功，用户{0}钱包余额增加{1},目前钱包余额为{2}'.format(effect_user.username,
                                                                   money_change_log.changeAmount,
                                                                   money_change_log.remainAmount)

        return Response({'message': success_message}, status=status.HTTP_200_OK)


class CoinChangLogViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.AllowAny,)    #  调试模式
    # permission_classes = (permissions.IsAuthenticated,)  #  正式环境
    serializer_class = CoinLogListSerializer
    filter_class = CoinChangLogListFilter
    queryset = CoinChangeLog.objects.filter().order_by(*['-created_time', '-id'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(user=1))
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        return Response(self.get_paginated_response(serializer.data).data)

