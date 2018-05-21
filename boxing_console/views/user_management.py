# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import User
from rest_framework import viewsets, filters
from boxing_console.serializers import UserSerializer
from boxing_console.filters import UserFilter


class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("id", "mobile", "user_profile__nick_name")
    filter_class = UserFilter
