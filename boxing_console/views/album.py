# -*- coding=utf-8 -*-

from rest_framework import viewsets
from biz import models
from boxing_console.serializers import AlbumSerializer
from boxing_console.serializers import AlbumPictureSerializer
from rest_framework.response import Response


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = models.Album.objects.select_related('related_account', 'related_account__user_profile')


class AlbumPictureViewSet(viewsets.ViewSet):

    def list(self, request, album_id):
        queryset = models.AlbumPicture.objects.filter(album=album_id)
        serializer = AlbumPictureSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, album_id):
        serializer = AlbumPictureSerializer(data=request.data)
        if serializer.is_valid():
            pic = models.AlbumPicture(album_id=int(album_id), picture=serializer.validated_data['picture'])
            pic.save()
            return Response(pic.id, status=201)

        return Response(status=400)

    def delete(self, request, picture_id):
        models.AlbumPicture.objects.filter(id=picture_id).delete()
        return Response(status=200)

