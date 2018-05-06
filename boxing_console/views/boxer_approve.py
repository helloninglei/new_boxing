from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from biz.constants import OperationType
from biz.models import BoxerIdentification, User
from biz.services.operation_log_service import log_boxer_identification_operation
from boxing_console.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('is_professional_boxer', 'authentication_state', 'lock_state')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')

    def order_lock(self, request, *args, **kwargs):
        isinstance = self.get_object()
        isinstance.lock_state = True
        isinstance.save()
        log_boxer_identification_operation(identification_id=isinstance.pk,
                                           operator=User.objects.get(pk=1),
                                           operation_type=OperationType.BOXER_ORDER_LOCK,
                                           content="拳手接单状态锁定")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def order_unlock(self, request, *args, **kwargs):
        isinstance = self.get_object()
        isinstance.lock_state = False
        isinstance.save()
        log_boxer_identification_operation(identification_id=self.get_object().pk,
                                           operator=User.objects.get(pk=1),
                                           operation_type=OperationType.BOXER_ORDER_UNLOCK,
                                           content="拳手接单状态解锁")
        return Response(status=status.HTTP_204_NO_CONTENT)

    def approve(self, request, *args, **kwargs):
        kwargs['authentication_state'] = OperationType.BOXER_AUTHENTICATION_APPROVED
        super().partial_update(request, *args, **kwargs)
        log_boxer_identification_operation(self.get_object().pk, request.user, OperationType.BOXER_ORDER_LOCK, None)

        return Response(reverse('boxer_identification_list'))

    def refuse(self, request, *args, **kwargs):
        kwargs['authentication_state'] = OperationType.BOXER_AUTHENTICATION_REFUSE
        super().partial_update(request, *args, **kwargs)
        log_boxer_identification_operation(self.get_object().pk, request.user, OperationType.BOXER_ORDER_LOCK,
                                           kwargs['refuse_reason'])
        return Response(reverse('boxer_identification_list'))
