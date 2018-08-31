# -*- coding: utf-8 -*-
from django.db.models import Count, Q, ExpressionWrapper, F, IntegerField
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from biz.models import Message
from boxing_app.serializers import MessageSerializer
from boxing_app.permissions import OnlyOwnerCanDeletePermission
from biz.redis_client import following_list_all, blocked_user_list
from biz.utils import comment_count_condition


class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = (OnlyOwnerCanDeletePermission, IsAuthenticatedOrReadOnly)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def get_object(self):
        self.queryset = self._get_query_set().filter(pk=self.kwargs['pk'])
        return super().get_object()

    def destroy(self, request, *args, **kwargs):
        self.get_object().soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def _get_query_set(self):
        user_id = self.request.user.id
        blocked_user_id_list = blocked_user_list(user_id)
        is_like = Count('likes', filter=Q(likes__user_id=user_id), distinct=True)
        return Message.objects.exclude(user_id__in=blocked_user_id_list).annotate(
            like_count=ExpressionWrapper(Count('likes', distinct=True) + F('initial_like_count'),
                                         output_field=IntegerField()), comment_count=comment_count_condition,
            is_like=is_like).select_related('user__boxer_identification', 'user__user_profile')

    def search_message(self, request, *args, **kwargs):
        keywords = self.request.query_params.get('keywords', "")
        self.queryset = self._get_query_set().filter(content__icontains=keywords) if keywords else []
        return super().list(request, *args, **kwargs)

    # 最新动态
    def list(self, request, *args, **kwargs):
        user_id = request.query_params.get('user_id')
        if user_id:  # 指定用户的动态
            self.queryset = self._get_query_set().filter(user_id=user_id)
        else:
            self.queryset = self._get_query_set()
        return super().list(request, *args, **kwargs)

    def hot(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().order_by('-like_count', '-created_time')
        return super().list(request, *args, **kwargs)

    def following(self, request, *args, **kwargs):
        user_id_list = following_list_all(request.user.id)
        self.queryset = self._get_query_set().filter(user_id__in=user_id_list)
        return super().list(request, *args, **kwargs)

    def mine(self, request, *args, **kwargs):
        self.queryset = self._get_query_set().filter(user_id=request.user.id)
        return super().list(request, *args, **kwargs)
