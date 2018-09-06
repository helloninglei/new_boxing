# -*- coding:utf-8 -*-
from rest_framework import viewsets, permissions
from biz.models import Album, AlbumPicture
from boxing_app.serializers import AlbumSerializer, AlbumPictureSerilizer
from rest_framework.pagination import PageNumberPagination


class AlbumPageNumberPagination(PageNumberPagination):
    page_size = 5


class AlbumPicturePageNumberPagination(PageNumberPagination):
    page_size = None


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = AlbumPageNumberPagination

    def get_queryset(self):
        return Album.objects.filter(related_account_id=self.kwargs['pk']).prefetch_related('pictures')


class AlbumPictureViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumPictureSerilizer
    permission_classes = (permissions.AllowAny,)
    pagination_class = AlbumPicturePageNumberPagination

    def get_queryset(self):
        return AlbumPicture.objects.filter(album_id=self.kwargs['pk'])
