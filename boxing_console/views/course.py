from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from biz.models import Course, CourseSettleOrder, CourseOrder
from boxing_console.filters import CourseFilter, CourseOrderFilter, CourseSettleOrderFilter
from boxing_console.serializers import CourseSerializer, CourseOrderSerializer, CourseSettleOrderSerializer, \
    CourseOrderInsuranceSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filter_class = CourseFilter
    search_fields = ('boxer__real_name', 'boxer__mobile')


class CourseOrderViewSet(viewsets.ModelViewSet):
    serializer_class = CourseOrderSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('user__mobile', 'course__boxer__real_name', 'course__boxer__mobile', 'user__user_profile__name',
                     'user__user_profile__nick_name')
    filter_class = CourseOrderFilter

    def get_queryset(self):
        return CourseOrder.objects.all().select_related('boxer', 'user', 'club')

    def mark_insurance(self, request, *args, **kwargs):
        serializer = CourseOrderInsuranceSerializer(data=request.data, context={'order': self.get_object()})
        serializer.is_valid(raise_exception=True)
        CourseOrder.objects.filter(pk=kwargs['pk']).update(
            insurance_amount=serializer.validated_data['insurance_amount'])
        return Response({'message': '成功添加保险'}, status=status.HTTP_204_NO_CONTENT)


class CourseSettleOrderViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CourseSettleOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = CourseSettleOrderFilter
    queryset = CourseSettleOrder.objects.all().prefetch_related('course', 'order', 'order__user', 'course__boxer')
