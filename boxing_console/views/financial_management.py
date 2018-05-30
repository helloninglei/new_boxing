from django.db.models import Q
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import WithdrawLog, PayOrder
from boxing_console.serializers import WithdrawLogSerializer, PayOrdersReadOnlySerializer
from boxing_console.filters import WithdrawLogFilter


class WithdrawLogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = WithdrawLog.objects.all().order_by("-created_time")
    serializer_class = WithdrawLogSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["order_number", "user__id", "user__user_profile__nick_name", "user__mobile"]
    filter_class = WithdrawLogFilter

    def get_serializer_context(self):
        serializer_context = super().get_serializer_context()
        serializer_context.update(operate_type=self.kwargs.get("operate"))
        return serializer_context


class PayOrdersViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = PayOrder.objects.filter(~Q(content_type__model="user")).order_by("-order_time")
    serializer_class = PayOrdersReadOnlySerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ['user__id', "user__mobile", "user__user_profile__nick_name", "out_trade_no"]
    filter_fields = ["device", "payment_type", "status"]
