# -*- coding:utf-8 -*-
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from biz.models import Album, AlbumPicture
from boxing_app.serializers import AlbumSerializer
from boxing_app.pagination import BoxingPagination


class AlbumPageNumberPagination(BoxingPagination):
    page_size = 5


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = AlbumPageNumberPagination

    def get_queryset(self):
        return Album.objects.filter(related_account_id=self.kwargs['pk'], is_show=True).prefetch_related('pictures')


@api_view(['GET'])
@permission_classes([])
def picture_list(request, pk):
    return Response({'results': [item for item in AlbumPicture.objects.filter(album_id=pk).values_list('picture', flat=True)]})
