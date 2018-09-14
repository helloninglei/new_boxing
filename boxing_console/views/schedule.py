from rest_framework import generics
from boxing_console.serializers import ScheduleCommonSerializer
from biz.models import Schedule


class ScheduleListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ScheduleCommonSerializer
    queryset = Schedule.objects.all().order_by("-race_date")

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)


class ScheduleUpdateApiView(generics.UpdateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleCommonSerializer
