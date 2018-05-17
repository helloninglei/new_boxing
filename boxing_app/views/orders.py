from rest_framework import viewsets

from biz.models import BoxerIdentification, PayOrder
from boxing_app.serializers import BoxerCourseOrderSerializer


class BoxerCourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerCourseOrderSerializer

    def get_queryset(self):
        boxer = BoxerIdentification.objects.get(user=self.request.user)
        return PayOrder.objects.filter(course__boxer=boxer)
