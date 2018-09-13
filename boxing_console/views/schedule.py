from rest_framework import generics
from boxing_console.serializers import ScheduleSerializer
from biz.models import Schedule


class ScheduleListCreateApiView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all().order_by("-race_date")

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)
