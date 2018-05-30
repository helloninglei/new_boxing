# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import User, MoneyChangeLog
from rest_framework import viewsets, filters, mixins
from boxing_console.serializers import UserSerializer, MoneyBalanceChangeLogSerializer
from boxing_console.filters import UserFilter, MoneyChangeLogFilter


class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().select_related("user_profile", "boxer_identification").order_by("-date_joined")
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("id", "mobile", "user_profile__nick_name")
    filter_class = UserFilter


class MoneyBalanceChangeLogViewSet(viewsets.GenericViewSet,
                                   mixins.ListModelMixin):

    serializer_class = MoneyBalanceChangeLogSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = MoneyChangeLogFilter

    def get_queryset(self):
        return MoneyChangeLog.objects.filter(user=self.kwargs['pk'])
