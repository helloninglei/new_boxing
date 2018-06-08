
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response

from biz import constants
from biz.models import BoxerIdentification, PayOrder, Course, OrderComment, CourseOrder
from biz.services.pay_service import PayService
from boxing_app.permissions import OnlyBoxerSelfCanConfirmOrderPermission, OnlyUserSelfCanConfirmOrderPermission
from boxing_app.serializers import BoxerCourseOrderSerializer, UserCourseOrderSerializer, CourseOrderCommentSerializer


class BaseCourseOrderViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("status",)


class BoxerCourseOrderViewSet(BaseCourseOrderViewSet):
    serializer_class = BoxerCourseOrderSerializer

    def get_queryset(self):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        return CourseOrder.objects.filter(boxer=boxer)

    @permission_classes([OnlyBoxerSelfCanConfirmOrderPermission])
    def boxer_confirm_order(self, request, *args, **kwargs):
        course_order = self.get_object()
        if course_order.status != constants.PAYMENT_STATUS_WAIT_USE:
            return Response({"message": "订单状态不是未使用状态，无法确认"}, status=status.HTTP_400_BAD_REQUEST)
        course_order.confirm_status = constants.COURSE_ORDER_STATUS_BOXER_CONFIRMED
        course_order.save()
        # TODO:创建定时任务
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCourseOrderViewSet(BaseCourseOrderViewSet):
    serializer_class = UserCourseOrderSerializer

    def get_queryset(self):
        return CourseOrder.objects.filter(user=self.request.user)

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
        if instance.status != constants.PAYMENT_STATUS_UNPAID:
            return Response({"message":'订单不是未支付状态，不能删除'}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @permission_classes([OnlyUserSelfCanConfirmOrderPermission])
    def user_confirm_order(self, request, *args, **kwargs):
        course_order = self.get_object()
        if course_order.status != constants.COURSE_PAYMENT_STATUS_WAIT_USE:
            return Response({"message": "只有待使用的订单才能进行确认"}, status=status.HTTP_400_BAD_REQUEST)
        if course_order.confirm_status != constants.COURSE_ORDER_STATUS_BOXER_CONFIRMED:
            return Response({"message": "拳手确认完成后才能确认"}, status=status.HTTP_400_BAD_REQUEST)
        course_order.confirm_status = constants.COURSE_ORDER_STATUS_USER_CONFIRMED
        course_order.save()
        course_order.pay_order.status = constants.PAYMENT_STATUS_WAIT_COMMENT
        course_order.pay_order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseOrderCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderCommentSerializer

    def get_queryset(self):
        return OrderComment.objects.filter(order_id=self.kwargs['order_id'])

    def perform_create(self, serializer):
        self.do_order_finish(self.kwargs['order_id'])
        serializer.save(user=self.request.user)

    def do_order_finish(self, order_id):
        PayOrder.objects.filter(id=order_id).update(status=constants.PAYMENT_STATUS_FINISHED)
