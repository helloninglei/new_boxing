from django.contrib.contenttypes.models import ContentType
from rest_framework import viewsets

from biz.models import BoxerIdentification, PayOrder, Course
from boxing_app.serializers import BoxerCourseOrderSerializer, UserCourseOrderSerializer


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