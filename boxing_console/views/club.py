from django.db.transaction import atomic
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from biz import redis_client
from biz.models import BoxingClub, Course
from boxing_console.serializers import BoxingClubSerializer


class BoxingClubVewSet(viewsets.ModelViewSet):
    serializer_class = BoxingClubSerializer
    queryset = BoxingClub.all_objects.all().order_by('-id')
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)

    def update(self, request, *args, **kwargs):
        club = self.get_object()
        self.record_club_boxer_location(club)
        return super().update(request, *args, **kwargs)

    def operate(self, request, *args, **kwargs):
        operate = kwargs['operate']
        return self.close_club() if operate == 'close' else self.open_club()

    @atomic
    def close_club(self):
        club = self.get_object()
        self.del_club_and_location(club)
        self.del_club_boxer_location(club)
        self.close_club_courses(club)
        self.close_boxer_accept_order_status(club)
        return Response({"message": "拳馆已关闭"}, status=status.HTTP_204_NO_CONTENT)

    @atomic
    def open_club(self):
        club = BoxingClub.all_objects.get(id=self.kwargs['pk'])
        self.open_club_and_record_location(club)
        self.record_club_boxer_location(club)
        return Response({"message": "拳馆已开启"}, status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def del_club_and_location(club):
        club.soft_delete()
        redis_client.del_object_location(club)

    @staticmethod
    def del_club_boxer_location(club):
        courses = Course.objects.filter(club=club.id).select_related('boxer')
        for course in courses:
            redis_client.del_object_location(course.boxer)

    @staticmethod
    def close_club_courses(club):
        Course.objects.filter(club=club.id).update(is_open=False)

    @staticmethod
    def close_boxer_accept_order_status(club):
        courses = Course.objects.filter(club=club.id).select_related('boxer')
        for course in courses:
            course.boxer.is_accept_order = False
            course.boxer.save()

    @staticmethod
    def open_club_and_record_location(club):
        club.is_deleted = False
        club.save()
        redis_client.record_object_location(club, club.longitude, club.latitude)

    @staticmethod
    def record_club_boxer_location(club):
        courses = Course.objects.filter(club=club, is_open=True).select_related('boxer')
        for course in courses:
            redis_client.record_object_location(course.boxer, club.longitude, club.latitude)
