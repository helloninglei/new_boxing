from rest_framework import viewsets, status
from rest_framework.response import Response

from biz.redis_client import get_shutup_list, rm_shutup_list, add_shutup_list
from boxing_app.serializers import UserProfileSerializer, ShutUpWriteOnlySerializer


class ShutUpListViewSet(viewsets.GenericViewSet):
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        return get_shutup_list()

    def list(self, request):
        return Response({"results": self.get_queryset()}, status=status.HTTP_200_OK)

    def destroy(self, request):
        serializer = ShutUpWriteOnlySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        rm_shutup_list(*serializer.validated_data['user_ids'])
        return Response({"message": "解禁成功"}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request):
        serializer = ShutUpWriteOnlySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        add_shutup_list(*serializer.validated_data['user_ids'])
        return Response({"message": "禁言成功"}, status=status.HTTP_201_CREATED)
