# -*- coding:utf-8 -*-
from rest_framework import viewsets, permissions
from biz.models import Album, AlbumPicture
from boxing_app.serializers import AlbumSerializer
from rest_framework.pagination import PageNumberPagination
from django.http import JsonResponse


class AlbumPageNumberPagination(PageNumberPagination):
    page_size = 5


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = AlbumPageNumberPagination

    def get_queryset(self):
        return Album.objects.filter(related_account_id=self.kwargs['pk']).prefetch_related('pictures')


def picture_list(request, pk):
    return JsonResponse({'results': [item.picture for item in AlbumPicture.objects.filter(album_id=pk)]}, status=200)
