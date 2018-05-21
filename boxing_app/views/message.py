# -*- coding: utf-8 -*-
from django.db.models import Count, Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from biz.models import Message
from boxing_app.serializers import MessageSerializer
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from biz.redis_client import following_list_all


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission,)

    queryset = Message.objects.all().prefetch_related('user')
    serializer_class = MessageSerializer

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _get_query_set(self):
        user = self.request.user
        is_like = Count('likes', filter=Q(likes__user=user))
        return Message.objects.annotate(like_count=Count('likes'), comment_count=Count('comments'),
                                        is_like=is_like).prefetch_related('user__boxer_identification')

    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        self.queryset = self._get_query_set().filter(user_id=user_id) if user_id else self._get_query_set()
        return super().list(request, *args, **kwargs)

    def hot(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().order_by('-like_count')
        return super().list(request, *args, **kwargs)

    def followed(self, request, *args, **kwargs):
        user_id_list = following_list_all(request.user.id)
        self.queryset = self._get_query_set().filter(user_id__in=user_id_list)
        return super().list(request, *args, **kwargs)

    def mine(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().filter(user=request.user)
        return super().list(request, *args, **kwargs)
