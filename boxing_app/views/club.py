from django.db.models import Case, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from biz.models import BoxingClub
from biz import redis_client
from boxing_app.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    filter_fields = ('city',)

    def get_queryset(self):
        longitude = self.request.query_params.get('longitude')
        latitude = self.request.query_params.get('latitude')
        if longitude and latitude:
            club_list = redis_client.get_near_object(BoxingClub, longitude, latitude)
            sort_rule = Case(*[When(pk=pk, then=distance) for pk, distance in club_list])
            return self.queryset.order_by(sort_rule, '-id')
        return self.queryset
