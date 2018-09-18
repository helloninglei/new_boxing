from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from boxing_console.serializers import ScheduleCommonSerializer, MatchCreateSerializer
from biz.models import Schedule, Player


class ScheduleListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ScheduleCommonSerializer
    queryset = Schedule.objects.all().order_by("-race_date")

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)


class ScheduleUpdateRetrieveDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCommonSerializer


class MatchCreateApiView(generics.CreateAPIView):
    serializer_class = MatchCreateSerializer


@api_view(['GET'])
def players(_):
    return Response({"results": Player.objects.values("id", "name", "mobile")})
