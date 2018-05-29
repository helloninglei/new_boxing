from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import WithdrawLog
from boxing_console.serializers import WithdrawLogSerializer
from boxing_console.filters import WithdrawLogFilter


class WithdrawLogViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = WithdrawLog.objects.all().order_by("-created_time")
    serializer_class = WithdrawLogSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["order_number", "user__id", "user__user_profile__nick_name", "user__mobile"]
    filter_class = WithdrawLogFilter
