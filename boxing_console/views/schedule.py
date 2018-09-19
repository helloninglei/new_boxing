from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from boxing_console.serializers import ScheduleCommonSerializer, MatchCommonSerializer, SchedulePatchUpdateSerializer
from biz.models import Schedule, Player, Match


class ScheduleListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ScheduleCommonSerializer
    queryset = Schedule.objects.all().order_by("-race_date")

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)


class ScheduleUpdateRetrieveDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCommonSerializer

    def perform_update(self, serializer):
        serializer.save(operator=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        self.serializer_class = SchedulePatchUpdateSerializer
        return super(ScheduleUpdateRetrieveDestroyApiView, self).partial_update(request, *args, **kwargs)


class MatchCreateApiView(generics.CreateAPIView):
    serializer_class = MatchCommonSerializer


class MatchRetrieveApiView(generics.RetrieveAPIView):
    queryset = Match.objects.all()
    serializer_class = MatchCommonSerializer


@api_view(['GET'])
def players(_):
    return Response({"results": Player.objects.values("id", "name", "mobile")})
