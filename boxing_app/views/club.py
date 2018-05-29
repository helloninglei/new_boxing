from rest_framework import viewsets, filters
from rest_framework.viewsets import GenericViewSet

from biz.models import BoxingClub
from boxing_app.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)
