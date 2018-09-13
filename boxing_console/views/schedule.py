from rest_framework import generics
from boxing_console.serializers import ScheduleSerializer


class ScheduleCreateApiView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer

    def perform_create(self, serializer):
        serializer.save(operator=self.request.user)
