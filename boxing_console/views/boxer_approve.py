from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.reverse import reverse


from biz import constants, sms_client
from biz.constants import OperationType, BOXER_ALLOWED_COURSES_CHOICE
from biz.models import BoxerIdentification, Course
from biz.services.operation_log_service import log_boxer_identification_operation
from boxing_console.serializers import BoxerIdentificationSerializer, CourseSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all().order_by('-updated_time')
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('is_professional_boxer', 'authentication_state', 'is_locked')
    search_fields = ('user__mobile', 'real_name', 'user__user_profile__nick_name')

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
            operation_type = OperationType.BOXER_AUTHENTICATION_APPROVED
            content = request.data.get('allowed_course')
            course_dict = dict(BOXER_ALLOWED_COURSES_CHOICE)
            allowed_courses = [course_dict.get(key) for key in content]
            self.create_course(boxer=boxer, allowed_courses=content)
            sms_client.send_boxer_approved_message(boxer.mobile, allowed_courses='、'.join(allowed_courses))
        else:
            operation_type = OperationType.BOXER_AUTHENTICATION_REFUSE
            content = request.data.get('refuse_reason')
            sms_client.send_boxer_refuse_message(boxer.mobile, refuse_reason=content)
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
