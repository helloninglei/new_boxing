from django.db.models import When, Case, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.reverse import reverse

from biz import redis_client
from biz import constants, sms_client
from biz.constants import OperationType, BOXER_ALLOWED_COURSES_CHOICE, USER_TYPE_BOXER
from biz.models import BoxerIdentification, Course
from biz.services.operation_log_service import log_boxer_identification_operation
from boxing_console.serializers import BoxerIdentificationSerializer, CourseSerializer, BoxerApproveSerializer, \
    BoxerRefuseSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerIdentificationSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('is_professional_boxer', 'authentication_state', 'is_locked')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')

    def get_queryset(self):
        sort_by_status = Case(When(authentication_state=constants.BOXER_AUTHENTICATION_STATE_WAITING, then=1),
                              default=2)
        return BoxerIdentification.objects.all().order_by(sort_by_status, '-updated_time')

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
        boxer = self.get_object()
        if is_approve:
            serializer = BoxerApproveSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            operation_type = OperationType.BOXER_AUTHENTICATION_APPROVED
            content = allowed_courses = serializer.validated_data['allowed_course']
            title = serializer.validated_data['title']
            self.create_course(boxer=boxer, allowed_courses=allowed_courses)
            self.alter_user_info(user=boxer.user, title=title)
            redis_client.del_user_title(boxer.user)
            sms_client.send_boxer_approved_message(boxer.mobile, allowed_courses='、'.join(allowed_courses))
        else:
            serializer = BoxerRefuseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            operation_type = OperationType.BOXER_AUTHENTICATION_REFUSE
            content = refuse_reason = serializer.validated_data['refuse_reason']
            sms_client.send_boxer_refuse_message(boxer.mobile, refuse_reason=refuse_reason)
        log_boxer_identification_operation(identification_id=self.get_object().pk,
                                           operator=request.user,
                                           operation_type=operation_type,
                                           content=content)
        return Response(reverse('boxer_identification_list'))

    @staticmethod
    def create_course(boxer, allowed_courses):
        Course.objects.filter(boxer=boxer).update(is_deleted=True)
        for course_name in allowed_courses:
            serializer = CourseSerializer(data={"course_name": course_name})
            serializer.is_valid(raise_exception=True)
            serializer.save(boxer=boxer)

    @staticmethod
    def alter_user_info(user, title):
        user.title = title
        user.user_type = USER_TYPE_BOXER
        user.save()

