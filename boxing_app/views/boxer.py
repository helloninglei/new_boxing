# -*- coding: utf-8 -*-
from datetime import datetime

from django.db.models import Case, When, Count, Min, Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, mixins, permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import get_object_or_404
from biz import constants, redis_client
from biz.constants import COURSE_PAYMENT_STATUS_UNPAID
from biz.models import BoxerIdentification
from boxing_app.filters import NearbyBoxerFilter
from boxing_app.permissions import IsBoxerPermission
from boxing_app.serializers import BoxerIdentificationSerializer, NearbyBoxerIdentificationSerializer


@api_view(['GET'])
def get_boxer_status(request):
    data = {'boxer_status': None}
    boxer = BoxerIdentification.objects.filter(user=request.user).only('authentication_state').first()
    if boxer:
        data.update(boxer_status=boxer.authentication_state)
    return Response(data=data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsBoxerPermission])
def change_boxer_accept_order_status(request, **kwargs):
    is_accept = True if kwargs.get('is_accept') == 'open' else False
    BoxerIdentification.objects.filter(user=request.user.id).update(is_accept_order=is_accept)
    return Response(status=status.HTTP_204_NO_CONTENT)


class BoxerIdentificationViewSet(viewsets.ModelViewSet):
    serializer_class = BoxerIdentificationSerializer

    def get_object(self):
        return BoxerIdentification.objects.get(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.authentication_state == constants.BOXER_AUTHENTICATION_STATE_WAITING:
            return Response({"message": "存在待审核的认证信息，不能修改"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, id=self.request.user.id)


class NearbyBoxerListViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = NearbyBoxerIdentificationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = BoxerIdentification.objects.filter(course__is_open=True,
                                                  course__is_deleted=False,
                                                  course__validity__gte=datetime.today(),
                                                  is_accept_order=True,
                                                  authentication_state=constants.BOXER_AUTHENTICATION_STATE_APPROVED,
                                                  is_locked=False)\
        .prefetch_related('course__club')\
        .select_related('user', 'user__user_profile') \
        .annotate(order_count=Count('boxer_course_order', distinct=True,
                                    filter=Q(boxer_course_order__status__gt=COURSE_PAYMENT_STATUS_UNPAID,
                                             boxer_course_order__is_deleted=False)),
                  min_price=Min('course__price', filter=Q(course__is_deleted=False, course__is_open=True)))\
        .distinct()
    filter_backends = (DjangoFilterBackend,)
    filter_class = NearbyBoxerFilter

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        if longitude and latitude:
            boxer_list = redis_client.get_near_object(BoxerIdentification, longitude, latitude)
            boxer_id_list = [item[0] for item in boxer_list]
            sort_rule = Case(*[When(pk=pk, then=distance) for pk, distance in boxer_list])
            return self.queryset.filter(id__in=boxer_id_list).order_by(sort_rule, '-order_count', 'min_price', 'created_time')
        return self.queryset.order_by('-order_count', 'min_price', 'created_time')


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def boxer_info_to_share(request, pk):
    boxer = get_object_or_404(BoxerIdentification, pk=pk)
    serializer = BoxerIdentificationSerializer(boxer)
    return Response({"results": serializer.data})
