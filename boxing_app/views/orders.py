from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets

from biz import constants
from biz.models import BoxerIdentification, PayOrder, Course, OrderComment
from boxing_app.serializers import BoxerCourseOrderSerializer, UserCourseOrderSerializer, CourseOrderCommentSerializer


class BoxerCourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerCourseOrderSerializer

    def get_queryset(self):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        return PayOrder.objects.filter(course__boxer=boxer)


class UserCourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = UserCourseOrderSerializer

    def get_queryset(self):
        content_type = ContentType.objects.get_for_model(Course)
        return PayOrder.objects.filter(content_type=content_type, user=self.request.user)


class CourseOrderCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderCommentSerializer

    def get_queryset(self):
        return OrderComment.objects.filter(order_id=self.kwargs['order_id'])

    def perform_create(self, serializer):
        self.do_order_finish(self.kwargs['order_id'])
        serializer.save(user=self.request.user)

    def do_order_finish(self, order_id):
        order = PayOrder.objects.get(id=order_id)
        order.status = constants.PAYMENT_STATUS_FINISHED
        order.save()