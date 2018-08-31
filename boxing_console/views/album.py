# -*- coding=utf-8 -*-

from rest_framework import viewsets
from biz import models
from boxing_console.serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = models.Album.objects.all()
