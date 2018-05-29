# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from biz.models import Message
from boxing_app.serializers import MessageSerializer
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from biz.redis_client import following_list_all


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission, IsAuthenticatedOrReadOnly)

    queryset = Message.objects.all().prefetch_related('user')
    serializer_class = MessageSerializer

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _get_query_set(self):
        user_id = self.request.user.id
        is_like = Count('likes', filter=Q(likes__user_id=user_id), distinct=True)
        return Message.objects.annotate(like_count=Count('likes', distinct=True), comment_count=Count('comments', distinct=True),
                                        is_like=is_like).prefetch_related('user__boxer_identification',
                                                                          'user__user_profile')

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        self.queryset = self._get_query_set().filter(user_id=user_id) if user_id else self._get_query_set()
        return super().list(request, *args, **kwargs)

    def hot(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().order_by('-like_count')
        return super().list(request, *args, **kwargs)

    def following(self, request, *args, **kwargs):
        user_id_list = following_list_all(request.user.id)
        self.queryset = self._get_query_set().filter(user_id__in=user_id_list)
        return super().list(request, *args, **kwargs)

    def mine(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().filter(user=request.user)
        return super().list(request, *args, **kwargs)
