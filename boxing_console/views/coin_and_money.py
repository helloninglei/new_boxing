# -*- coding: utf-8 -*-
from rest_framework import permissions, mixins
from rest_framework.viewsets import GenericViewSet

from biz.models import CoinChangeLog, MoneyChangeLog
from boxing_console.filters import CoinChangLogListFilter
from boxing_console.serializers import  MoneyLogSerializer, CoinLogSerializer

class MoneyChangeLogViewSet(mixins.CreateModelMixin,
                            GenericViewSet):
    serializer_class = MoneyLogSerializer
    queryset = MoneyChangeLog.objects.all()


class CoinChangLogViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    serializer_class = CoinLogSerializer
    filter_class = CoinChangLogListFilter
    queryset = CoinChangeLog.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user.pk)
        return super(CoinChangLogViewSet, self).list(request, *args, **kwargs)


