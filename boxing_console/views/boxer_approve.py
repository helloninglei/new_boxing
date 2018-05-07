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
        instance.is_locked = True if kwargs['lock_type']==constants.OperationType.BOXER_ORDER_LOCK else False
        instance.save()
        log_boxer_identification_operation(identification_id=instance.pk,
                                           operator=request.user,
                                           operation_type=kwargs['lock_type'],
                                           content="拳手接单状态修改为：{}".format(kwargs['lock_type']))
        return Response(status=status.HTTP_204_NO_CONTENT)

    def approve(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        log_boxer_identification_operation(identification_id=self.get_object().pk,
                                           operator=request.user,
                                           operation_type=OperationType.BOXER_AUTHENTICATION_APPROVED,
                                           content="拳手认证信息审核通过,可开通课程为：{}".format(request.data.get('allow_lesson')))
        return Response(reverse('boxer_identification_list'))

    def refuse(self, request, *args, **kwargs):
        super().partial_update(request, *args, **kwargs)
        log_boxer_identification_operation(identification_id=self.get_object().pk,
                                           operator=request.user,
                                           operation_type=OperationType.BOXER_AUTHENTICATION_REFUSE,
                                           content="拳手认证信息审核失败，理由是：{}".format(request.data.get('refuse_reason')))
        return Response(reverse('boxer_identification_list'))
