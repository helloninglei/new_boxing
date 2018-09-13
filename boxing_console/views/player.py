from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from biz.models import Player, User
from boxing_console.serializers import PlayerSerializer


class PlayerViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    def perform_create(self, serializer):
        user = User.objects.get(mobile=serializer.validated_data["mobile"])
        serializer.save(user=user)
