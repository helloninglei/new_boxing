from rest_framework.decorators import api_view
from rest_framework import viewsets, mixins
from rest_framework import status
from rest_framework.response import Response
from boxing_app.serializers import BindAlipayAccountSerializer, UserProfileSerializer
from biz.models import UserProfile


@api_view(['POST'])
def bind_alipay_account(request):
    serializer = BindAlipayAccountSerializer(data=request.data, context={"user": request.user})
    serializer.is_valid(raise_exception=True)
    UserProfile.objects.update_or_create(user=request.user, alipay_account=serializer.validated_data['alipay_account'])
    return Response({"message": "ok"}, status=status.HTTP_200_OK)


class UserProfileViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return UserProfile.objects.get(user=self.request.user)
