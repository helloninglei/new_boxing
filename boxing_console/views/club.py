from django.db import transaction
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from biz import redis_client
from biz.models import BoxingClub
from boxing_console.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def close_club(self, request, *args, **kwargs):
        club = self.get_object()
        club.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
