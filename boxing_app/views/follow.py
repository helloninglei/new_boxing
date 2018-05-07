# -*- coding: utf-8 -*-
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, Q
from biz.models import User, Follow
from boxing_app.serializers import FollowedSerializer, FollowerSerializer


class BaseFollowViewSet(ModelViewSet):

    def perform_create(self, serializer):
        to_follow_user_id = self.request.POST['user_id']
        to_follow_user = User.objects.get(id=to_follow_user_id)
        follow_user = self.request.user
        kwargs = {
            'user': to_follow_user,
            'follower': follow_user
        }
        serializer.save(**kwargs)

    def _get_query_set(self, condition):
        user = self.request.user
        print(self.request.user)
        is_follow = Count('follower', filter=Q(follower__followed=user))
        return Follow.objects.filter(**condition).annotate(is_follow=is_follow).prefetch_related('user')


class FollowerViewSet(BaseFollowViewSet):
    serializer_class = FollowerSerializer

    def get_queryset(self):
        return self._get_query_set({'user': self.request.user})


class FollowedViewSet(BaseFollowViewSet):
    serializer_class = FollowedSerializer

    def get_queryset(self):
        return self._get_query_set({'follower': self.request.user})
