# -*- coding:utf-8 -*-
from rest_framework import viewsets, permissions
from biz.models import Album
from boxing_app.serializers import AlbumSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return Album.objects.filter(related_account_id=self.kwargs['pk']).prefetch_related('pictures')
