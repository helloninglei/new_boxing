from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from biz.models import User
from boxing_app.serializers import SocialLoginSerializer, MobileIsBindAnotherSocialAccountSerializer


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def social_login(request):
    serializer = SocialLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.filter(**serializer.validated_data).first()
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
    return Response({"token": ""})


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def mobile_is_bind_another_social_account(request):
    serializer = MobileIsBindAnotherSocialAccountSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    return Response({"result": User.objects.filter(**serializer.validated_data).exists()})
