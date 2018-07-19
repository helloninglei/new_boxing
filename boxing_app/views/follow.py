# -*- coding: utf-8 -*-
from django.db.models import Case, When, Value
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.conf import settings
from biz.models import User
from biz.redis_client import following_list, follower_list, follow_user, unfollow_user, follower_count, following_count, \
    follower_list_all
from boxing_app.serializers import FollowUserSerializer, ContactSerializer

PAGE_SIZE = settings.REST_FRAMEWORK['PAGE_SIZE']


class BaseFollowView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        page = int(request.query_params.get('page', 1))
        if self.__class__.list_type == 'follower':
            count_func, list_func = follower_count, follower_list
        else:
            count_func, list_func = following_count, following_list

        user_id = self.kwargs.get('user_id') or request.user.id
        user_id_list = list_func(user_id, page)
        has_more = count_func(user_id) > page * PAGE_SIZE
        return self._make_response(user_id_list, page, has_more)

    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        to_follow_user_id =request.data.get("user_id")
        if not User.objects.filter(pk=to_follow_user_id).exists():
            return Response({'message': '用户不存在'}, status=status.HTTP_400_BAD_REQUEST)
        follow_user(current_user_id, to_follow_user_id)
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request, *args, **kwargs):
        current_user_id = request.user.id
        following_user_id = request.data['user_id']
        unfollow_user(current_user_id, following_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _make_response(self, user_id_list, page, has_more):
        current_user_id = self.request.user.id
        user_list = User.objects.filter(id__in=user_id_list).select_related('boxer_identification',
                                                                            'user_profile').order_by("-date_joined")

        serializer = FollowUserSerializer(user_list, context={'current_user_id': current_user_id}, many=True)
        return Response({
            'page': page,
            'next': has_more,
            'result': serializer.data,
        })


class UnFollowView(APIView):
    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        following_user_id = request.data['user_id']
        unfollow_user(current_user_id, following_user_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowerView(BaseFollowView):
    list_type = 'follower'


class FollowingView(BaseFollowView):
    list_type = 'following'


@api_view(['GET'])
def contact_list(request):
    # 建群通讯录列表，即用户粉丝列表，不分页
    follower_ids = follower_list_all(request.user.id)
    user_list = User.objects.filter(id__in=follower_ids).select_related("user_profile").order_by(Case(
        When(user_profile__nick_name_index_letter="#", then=Value(chr(ord("Z") + 1))),
        default="user_profile__nick_name_index_letter"))
    serializer = ContactSerializer(user_list, many=True)
    return Response({"results": serializer.data}, status=status.HTTP_200_OK)
