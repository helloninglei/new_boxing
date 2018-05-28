from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from biz.models import MoneyChangeLog
from boxing_app.serializers import MoneyChangeLogReadOnlySerializer, WithdrawSerializer
from boxing_app.filters import MoneyChangeLogFilter
from biz.models import WithdrawLog


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
