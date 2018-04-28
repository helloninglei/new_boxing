import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets, permissions, filters

from biz.models import BoxerIdentification
from boxing_console.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(mixins.ListModelMixin,
                              mixins.RetrieveModelMixin,
                              viewsets.GenericViewSet):

    permission_classes = (permissions.AllowAny,)
    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all()
    filter_backends = (DjangoFilterBackend,filters.SearchFilter)
    filter_fields = ('is_professional_boxer','authentication_state','lock_state')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')
