
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from biz import constants
from biz.models import BoxerIdentification, PayOrder, Course, OrderComment, CourseOrder
from biz.services.pay_service import PayService
from boxing_app.permissions import OnlyBoxerSelfCanConfirmOrderPermission
from boxing_app.serializers import BoxerCourseOrderSerializer, UserCourseOrderSerializer, CourseOrderCommentSerializer, \
    PaySerializer


class BaseCourseOrderViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ("status",)


class BoxerCourseOrderViewSet(BaseCourseOrderViewSet):
    serializer_class = BoxerCourseOrderSerializer

    def get_queryset(self):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        return CourseOrder.objects.filter(boxer=boxer)

    @permission_classes([OnlyBoxerSelfCanConfirmOrderPermission])
    def confirm_order(self, pk):
        order = self.get_object()
        if order.status not in (constants.PAYMENT_STATUS_WAIT_USE, constants.PAYMENT_STATUS_WAIT_COMMENT):
            return Response({"message": "订单状态不是未使用状态，无法确认订单！"})

        # 修改订单状态
        # 创建定时任务
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


class CourseOrderCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderCommentSerializer

    def get_queryset(self):
        return OrderComment.objects.filter(order_id=self.kwargs['order_id'])

    def perform_create(self, serializer):
        self.do_order_finish(self.kwargs['order_id'])
        serializer.save(user=self.request.user)

    def do_order_finish(self, order_id):
        PayOrder.objects.filter(id=order_id).update(status=constants.PAYMENT_STATUS_FINISHED)
