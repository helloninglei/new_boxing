from rest_framework import filters
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet

from biz.models import Player, User
from boxing_console.serializers import PlayerSerializer


class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'mobile')

    def perform_create(self, serializer):
        user = User.objects.get(mobile=serializer.validated_data["mobile"])
        serializer.save(id=user.id, user=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.matches_red.exists() or instance.matches_blue.exists():
            raise ValidationError({"message": "请先删除该参赛拳手的所有赛程再删除拳手记录。"})
        return super().destroy(request, *args, **kwargs)
