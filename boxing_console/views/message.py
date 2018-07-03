# -*- coding: utf-8 -*-
from django.db.models import Count, F
from rest_framework import viewsets
from biz.models import Message
from boxing_console.serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        like_count = Count('likes', distinct=True)
        return Message.objects.annotate(like_count=like_count).select_related('user__boxer_identification',
                                                                              'user__user_profile')
