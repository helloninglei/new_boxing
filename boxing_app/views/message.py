# -*- coding: utf-8 -*-
from biz.models import Message
from django.db.models import Count
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from boxing_app.serializers import MessageSerializer
from boxing_app.permissions import OnlyOwnerCanDeletePermission

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission,)

    queryset = Message.objects.all().prefetch_related('user')
    serializer_class = MessageSerializer

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False)
    def hot(self, request, *args, **kwargs):
        self.queryset = Message.objects.annotate(like_count=Count('like')).order_by('-like_count')
        return super().list(request, *args, **kwargs)

