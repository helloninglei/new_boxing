# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from biz.models import User
from biz.redis_client import following_list, follower_list, follow_user, unfollow_user, follower_count, following_count
from boxing_app.serializers import FollowUserSerializer

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']


class BaseFollowView(APIView):
    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get('page', 1))
        if self.__class__.list_type == 'follower':
            count_func, list_func = follower_count, follower_list
        else:
            count_func, list_func = following_count, following_list
        user_id_list = list_func(request.user.id, page)
        has_more = count_func(request.user.id) > page * PAGE_SIZE
        return self._make_response(user_id_list, page, has_more)

    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        to_follow_user_id = int(request.data['user_id'])
        User.objects.get(pk=to_follow_user_id)
        if current_user_id == to_follow_user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follow_user(current_user_id, to_follow_user_id)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        current_user_id = request.user.id
        followed_user_id = request.data['user_id']
        unfollow_user(current_user_id, followed_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _make_response(self, user_id_list, page, has_more):
        current_user_id = self.request.user.id
        user_list = User.objects.filter(id__in=user_id_list)

        serializer = FollowUserSerializer(user_list, context={'current_user_id': current_user_id}, many=True)
        return Response({
            'page': page,
            'next': has_more,
            'result': serializer.data,
        })


class UnFollowView(APIView):
    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        followed_user_id = request.data['user_id']
        unfollow_user(current_user_id, followed_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowerView(BaseFollowView):
    list_type = 'follower'


class FollowedView(BaseFollowView):
    list_type = 'followed'
