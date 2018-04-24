# -*- coding: utf-8 -*-
from rest_framework import mixins, status, permissions, viewsets
from rest_framework.response import Response
from biz.models import CoinChangeLog, User
from boxing_console.filters import CoinChangLogListFilter
from boxing_console.serializers import CoinLogListSerializer, MoneySubstractSerializer, \
    CoinLogCreateSerializer


class UserCoinSubstract(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = CoinLogCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def add_or_substract(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        coin_change_log = serializer.save()
        success_message = u'操作成功，用户{0}拳豆增加{1},目前拳豆余额为{2}'.format(coin_change_log.user.mobile,
                                                                 coin_change_log.change_amount,
                                                                 coin_change_log.remain_amount)

        return Response({'message': success_message}, status=status.HTTP_200_OK)


class UserMoneySubstract(mixins.CreateModelMixin,
                         viewsets.GenericViewSet):
    serializer_class = MoneySubstractSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def add_or_substract(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        money_change_log = serializer.save()
        success_message = u'操作成功，用户{0}钱包金额增加{1}元,目前钱包余额为{2}元'.format(money_change_log.user.mobile,
                                                                   money_change_log.change_amount/100.00,
                                                                   money_change_log.remain_amount/100.00)

        return Response({'message': success_message}, status=status.HTTP_200_OK)


class CoinChangLogViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CoinLogListSerializer
    filter_class = CoinChangLogListFilter
    queryset = CoinChangeLog.objects.filter()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=self.request.user)
        return super(CoinChangLogViewSet, self).list(request, *args, **kwargs)