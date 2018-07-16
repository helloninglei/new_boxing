from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework.decorators import permission_classes, authentication_classes
from boxing_app.serializers import BindAlipayAccountSerializer, UserProfileSerializer, BlockedUserSerializer
from biz.models import UserProfile, User
from biz import redis_client
from biz.constants import USER_IDENTITY_DICT


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def user_profile_redirect(request, user_identity):
    user_id = USER_IDENTITY_DICT[user_identity]
    url = reverse('user-profile', kwargs={'pk': user_id})
    return redirect(url)


@api_view(['POST'])
def bind_alipay_account(request):
    serializer = BindAlipayAccountSerializer(data=request.data, context={"user": request.user})
    serializer.is_valid(raise_exception=True)
    UserProfile.objects.update_or_create(
        user=request.user, defaults={"alipay_account": serializer.validated_data['alipay_account']})
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.prefetch_related("user", "user__hot_videos")

    def get_object(self):
        return get_object_or_404(self.queryset, user=self.request.user)


class BlackListViewSet(viewsets.GenericViewSet):

    def list(self, request):
        blocked_user_list = User.objects.filter(
            id__in=redis_client.blocked_user_list(request.user.id)).prefetch_related("user_profile")
        return Response({"result": BlockedUserSerializer(blocked_user_list, many=True).data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        return Response({"result": redis_client.is_blocked(request.user.id, pk)}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        redis_client.unblock_user(request.user.id, pk)
        return Response(status=status.HTTP_200_OK)

    def create(self, request, pk):
        if redis_client.is_blocked(request.user.id, pk):
            return Response({"message": ["不能重复添加黑名单！"]}, status=status.HTTP_400_BAD_REQUEST)
        if pk in USER_IDENTITY_DICT.values():
            return Response({"message": ['官方账号不能加入黑名单!']}, status=status.HTTP_400_BAD_REQUEST)
        redis_client.block_user(request.user.id, pk)
        return Response(status=status.HTTP_201_CREATED)


class UserProfileNoLoginViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.prefetch_related("user", "user__hot_videos")
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return get_object_or_404(self.queryset, user=self.kwargs['pk'])


@api_view(['GET'])
@authentication_classes([])
@permission_classes([permissions.AllowAny])
def batch_user_profile(request):
    user_ids = request.query_params.get("user_ids", "")
    user_ids = user_ids.split(",")
    user_ids = [user_id for user_id in user_ids if user_id.isdigit()]

    users = UserProfile.objects.filter(user_id__in=user_ids).select_related("user",
                                                                            "user__boxer_identification")
    return Response({"results": UserProfileSerializer(users, many=True, context={"request": request}).data},
                    status=status.HTTP_200_OK)
