from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from biz.models import User, Player


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def check_player_mobile(request):
    mobile = request.query_params.get("mobile")
    is_player = Player.objects.filter(mobile=mobile).exists()
    is_user = User.objects.filter(mobile=mobile).exists()
    avatar = None
    if is_user:
        user = User.objects.get(mobile=mobile)
        avatar = user.user_profile.avatar
    return Response(data={"is_user": is_user, "is_player": is_player, "avatar": avatar}, status=status.HTTP_200_OK)
