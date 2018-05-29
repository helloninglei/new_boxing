from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response
from django.db.transaction import atomic
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import WithdrawLog
from boxing_console.serializers import WithdrawLogSerializer
from boxing_console.filters import WithdrawLogFilter
from biz.constants import WITHDRAW_STATUS_APPROVED, WITHDRAW_STATUS_REJECTED, \
    MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK
from biz.services.money_balance_service import change_money


class WithdrawLogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin):
    queryset = WithdrawLog.objects.all().order_by("-created_time")
    serializer_class = WithdrawLogSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["order_number", "user__id", "user__user_profile__nick_name", "user__mobile"]
    filter_class = WithdrawLogFilter

    @atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if kwargs['operate'] == "approved":
            instance.status = WITHDRAW_STATUS_APPROVED
            instance.save()
        if kwargs['operate'] == "rejected":
            instance.status = WITHDRAW_STATUS_REJECTED
            instance.save()
            change_money(request.user, instance.amount, MONEY_CHANGE_TYPE_INCREASE_REJECT_WITHDRAW_REBACK)

        return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
