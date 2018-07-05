# -*- coding: utf-8 -*-
from django.db.models import Count
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from biz.models import Message
from boxing_console.serializers import MessageSerializer
from boxing_console.filters import MessageFilter


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ["user__user_profile__nick_name", "user__mobile"]
    filter_class = MessageFilter

    def get_queryset(self):
        like_count = Count('likes', distinct=True)
        return Message.objects.annotate(like_count=like_count).select_related('user', 'user__boxer_identification',
                                                                              'user__user_profile')
