# -*- coding: utf-8 -*-
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from biz.models import User
from biz.redis_client import followed_list, follower_list, follow_user, unfollow_user
from boxing_app.serializers import FollowUserSerializer


class BaseFollowView(APIView):
    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        print(current_user_id)
        to_follow_user_id = request.data['user_id']
        if current_user_id == to_follow_user_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        follow_user(current_user_id, to_follow_user_id)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        current_user_id = request.user.id
        print(current_user_id)
        followed_user_id = request.data['user_id']
        unfollow_user(current_user_id, followed_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


    def _make_response(self, user_id_list):
        current_user_id = self.request.user.id
        user_list = User.objects.filter(id__in=user_id_list)
        serializer = FollowUserSerializer(user_list, context={'current_user_id': current_user_id}, many=True)
        return Response(serializer.data)


class FollowerView(BaseFollowView):
    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get('page', 1))
        user_id_list = follower_list(request.user.id, page)
        print(request.user.id)
        print(user_id_list)
        return self._make_response(user_id_list)


class FollowedView(BaseFollowView):
    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get('page', 1))
        user_id_list = followed_list(request.user.id, page)
        print(request.user.id)
        print(user_id_list)
        return self._make_response(user_id_list)
