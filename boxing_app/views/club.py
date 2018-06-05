from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import BoxingClub
from boxing_app.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    filter_fields = ('city',)
