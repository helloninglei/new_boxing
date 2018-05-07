from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import BoxerIdentification
from boxing_console.serializers import BoxerIdentificationSerializer


class BoxerIdentificationViewSet(viewsets.ModelViewSet):

    serializer_class = BoxerIdentificationSerializer
    queryset = BoxerIdentification.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('is_professional_boxer', 'authentication_state', 'lock_state')
    search_fields = ('mobile', 'real_name', 'user__user_profile__nick_name')
