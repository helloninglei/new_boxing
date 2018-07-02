# -*- coding: utf-8 -*-
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from biz.models import CoinChangeLog
from boxing_console.filters import CoinChangLogListFilter
from boxing_console.serializers import CoinLogSerializer


class CoinChangLogViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    serializer_class = CoinLogSerializer
    filter_class = CoinChangLogListFilter
    queryset = CoinChangeLog.objects.all()

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user.pk)
        return super(CoinChangLogViewSet, self).list(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)
