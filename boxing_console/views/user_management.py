# -*- coding: utf-8 -*-

from biz.models import User
from rest_framework import viewsets
from boxing_console.serializers import UserSerializer


class UserManagementViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
