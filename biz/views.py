# coding=utf-8
from django.http import JsonResponse
from rest_framework import permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from boxing_app.forms import UploadFileForm
from biz.services import file_service
from biz.serializers import AuthTokenLoginSerializer
from biz.services.captcha_service import get_captcha


@require_POST
def upload_file(request):
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
        urls = []
        for f in request.FILES.getlist('file'):
            url = file_service.save_upload_file(f)
            urls.append(url)
        data = {'urls': urls}
        if len(urls) == 1:
            data['url'] = url
        return JsonResponse(data)
    return JsonResponse({'message': form.errors})


class AuthTokenLogin(ObtainAuthToken):
    serializer_class = AuthTokenLoginSerializer
    authentication_classes = []


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def captcha_image(request):
    return Response(data=get_captcha(), status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(data={"message": "ok"}, status=status.HTTP_200_OK)
