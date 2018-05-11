from rest_framework import viewsets

from biz.models import BoxingClub
from boxing_console.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
