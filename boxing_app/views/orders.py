from datetime import datetime

from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from biz import constants, sms_client
from biz.models import BoxerIdentification, Course, OrderComment, CourseOrder, CourseSettleOrder, PayOrder
from biz.services.pay_service import PayService
from boxing_app.permissions import OnlyBoxerSelfCanConfirmOrderPermission, OnlyUserSelfCanConfirmOrderPermission
from boxing_app.serializers import BoxerCourseOrderSerializer, UserCourseOrderSerializer, CourseOrderCommentSerializer


class BaseCourseOrderViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("status",)


class BoxerCourseOrderViewSet(BaseCourseOrderViewSet):
    serializer_class = BoxerCourseOrderSerializer
    permission_classes = (OnlyBoxerSelfCanConfirmOrderPermission,)

    def get_queryset(self):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        return CourseOrder.objects.filter(boxer=boxer)

    def boxer_confirm_order(self, request, *args, **kwargs):
        course_order = self.get_object()
        if course_order.status != constants.COURSE_PAYMENT_STATUS_WAIT_USE:
            return Response({"message": "订单状态不是未使用状态，无法确认"}, status=status.HTTP_400_BAD_REQUEST)
        course_order.confirm_status = constants.COURSE_ORDER_STATUS_BOXER_CONFIRMED
        course_order.boxer_confirm_time = datetime.now()
        course_order.save()
        sms_client.send_boxer_confirmed_message(course_order.user.mobile, course_order)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCourseOrderViewSet(BaseCourseOrderViewSet):
    serializer_class = UserCourseOrderSerializer

    def get_queryset(self):
        return CourseOrder.objects.filter(user=self.request.user).select_related("boxer", "boxer__user",
                                                                                 "boxer__user__user_profile")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        course = get_object_or_404(Course, id=request.data.get('id'))
        if request.user == course.boxer.user:
            return Response({"message": "拳手不能购买自己的课程"}, status=status.HTTP_400_BAD_REQUEST)
        course_order_data = {
            "boxer": course.boxer.pk,
            "user": request.user.pk,
            "club": course.club.pk,
            "course": course.pk,
            "course_name": course.course_name,
            "course_price": course.price,
            "course_duration": course.duration,
            "course_validity": course.validity,
            "order_number": PayService.generate_out_trade_no()
        }
        serializer = self.get_serializer(data=course_order_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status != constants.COURSE_PAYMENT_STATUS_UNPAID:
            return Response({"message": '订单不是未支付状态，不能删除'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        pay_order = PayOrder.objects.filter(content_type__pk=ContentType.objects.get_for_model(instance).id,
                                            object_id=instance.id).first()
        if pay_order:
            pay_order.delete()
        super().perform_destroy(instance)

    @permission_classes([OnlyUserSelfCanConfirmOrderPermission])
    def user_confirm_order(self, request, *args, **kwargs):
        course_order = self.get_object()
        if course_order.status != constants.COURSE_PAYMENT_STATUS_WAIT_USE:
            return Response({"message": "只有待使用的订单才能进行确认"}, status=status.HTTP_400_BAD_REQUEST)
        if course_order.confirm_status != constants.COURSE_ORDER_STATUS_BOXER_CONFIRMED:
            return Response({"message": "拳手确认完成后才能确认"}, status=status.HTTP_400_BAD_REQUEST)
        course_order.confirm_status = constants.COURSE_ORDER_STATUS_USER_CONFIRMED
        course_order.status = constants.COURSE_PAYMENT_STATUS_WAIT_COMMENT
        course_order.user_confirm_time = datetime.now()
        course_order.save()
        self.create_settle_order(course_order)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def create_settle_order(course_order):
        CourseSettleOrder.objects.create(course=course_order.course,
                                         order=course_order.pay_order,
                                         course_order=course_order)


class CourseOrderCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderCommentSerializer

    def get_queryset(self):
        return OrderComment.objects.filter(order_id=self.kwargs['order_id']).select_related("order")

    def perform_create(self, serializer):
        self.do_order_finish(self.kwargs['order_id'])
        serializer.save(user=self.request.user)

    def do_order_finish(self, order_id):
        CourseOrder.objects.filter(id=order_id).update(status=constants.COURSE_PAYMENT_STATUS_FINISHED,
                                                       finish_time=datetime.now())
