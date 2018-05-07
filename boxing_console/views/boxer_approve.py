from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from biz import constants
from biz.constants import OperationType
from biz.models import BoxerIdentification
from biz.services.operation_log_service import log_boxer_identification_operation
from boxing_console.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('is_professional_boxer', 'authentication_state', 'is_locked')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')

    def change_lock_state(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_locked = True if kwargs['lock_type'] == constants.OperationType.BOXER_ORDER_LOCK else False
        instance.save()
        log_boxer_identification_operation(identification_id=instance.pk,
                                           operator=request.user,
                                           operation_type=kwargs['lock_type'],
                                           content="拳手接单状态修改为：{}".format(kwargs['lock_type']))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def approve(self, request, *args, **kwargs):
        return self.approved_or_refuse(request, True, *args, **kwargs)

    def refuse(self, request, *args, **kwargs):
        return self.approved_or_refuse(request, False, *args, **kwargs)

    def approved_or_refuse(self, request, is_approve, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        if is_approve:
            operation_type = OperationType.BOXER_AUTHENTICATION_APPROVED
            content = request.data.get('allow_lesson')
        else:
            operation_type = OperationType.BOXER_AUTHENTICATION_REFUSE
            content = request.data.get('refuse_reason')
        log_boxer_identification_operation(identification_id=self.get_object().pk,
                                           operator=request.user,
                                           operation_type=operation_type,
                                           content=content)
        return Response(reverse('boxer_identification_list'))
