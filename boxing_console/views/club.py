from django.db import transaction
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from biz.models import BoxingClub, Course
from boxing_console.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.objects.all()
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def operate(self, request, *args, **kwargs):
        operate = kwargs['operate']
        return self.close_club() if operate == 'close' else self.open_club()

    def close_club(self):
        club = self.get_object()
        club.soft_delete()
        Course.all_objects.filter(club=club.id).update(is_open=False)
        return Response({"message": "拳馆已关闭"}, status=status.HTTP_204_NO_CONTENT)

    def open_club(self):
        BoxingClub.all_objects.filter(id=self.kwargs['pk']).update(is_deleted=False)
        return Response({"message": "拳馆已开启"}, status=status.HTTP_204_NO_CONTENT)

