from datetime import datetime

from django.db.transaction import atomic
from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions, filters, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from biz import constants
from biz.models import BoxerIdentification, IdentificationOperateLog
from boxing_console.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all()
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    filter_fields = ('is_professional_boxer','approve_state','lock_state')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')

    def change_lock_state(self, request):
        self.create_operation_log(request=request, operate='lock')
        return Response(status=status.HTTP_204_NO_CONTENT)

    def approve(self, request):
        self.create_operation_log(request=request, operate='approve')
        return Response(reverse('boxer_identification_list'))

    def refuse(self, request, *args, **kwargs):
        self.create_operation_log(request=request, operate='refuse',operator_comment=kwargs.get('operator_comment'))
        return Response(reverse('boxer_identification_list'))

    @atomic
    def create_operation_log(self, request, operate, operator_comment=None):
        instance = self.get_object()
        operator = request.user
        state = None
        if operate=='lock':
            state = False if instance.lock_state else True
            instance.lock_state = state
        elif operate=='approve':
            state = constants.BOXER_APPROVE_STATE_APPROVED
            instance.approve_state = state
        elif operate=='refuse':
            state =  constants.BOXER_APPROVE_STATE_REFUSE
            instance.approve_state = state
            operate = 'approve'
        instance.save()

        operation_log = IdentificationOperateLog.objects.create(identification=instance,
                                                                operator=operator,
                                                                operator_comment=operator_comment)
        setattr(operation_log,'{}_state'.format(operate), state)
        operation_log.save()
