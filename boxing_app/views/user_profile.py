from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins, status, permissions
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from boxing_app.serializers import BindAlipayAccountSerializer, UserProfileSerializer, BlockedUserSerializer
from biz.models import UserProfile, User
from biz import redis_client
from biz.constants import USER_IDENTITY_DICT


@permission_classes([permissions.AllowAny])
@authentication_classes([])
@require_GET
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
    queryset = UserProfile.objects.all()

    def get_object(self):
        if "pk" in self.kwargs:
            return UserProfile.objects.filter(user=self.kwargs['pk']).first()
        return UserProfile.objects.get(user=self.request.user)


class BlackListViewSet(viewsets.GenericViewSet):

    def list(self, request):
        blocked_user_list = User.objects.filter(id__in=redis_client.blocked_user_list(request.user.id))
        return Response({"result": BlockedUserSerializer(blocked_user_list, many=True).data}, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        return Response({"result": redis_client.is_blocked(request.user.id, pk)}, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        redis_client.unblock_user(request.user.id, pk)
        return Response(status=status.HTTP_200_OK)

    def create(self, request, pk):
        redis_client.block_user(request.user.id, pk)
        return Response(status=status.HTTP_201_CREATED)
