from django.db import transaction
from rest_framework import viewsets

from biz import redis_client
from biz.models import BoxingClub
from boxing_console.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()

    @transaction.atomic
    def perform_destroy(self, instance):
        redis_client.del_boxing_club_location(instance.id)
        super().perform_destroy(instance)
