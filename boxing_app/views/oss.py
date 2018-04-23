# coding=utf-8
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from biz.services import aliyun_oss

@api_view(['GET'])
def get_upload_token(request):
    token = aliyun_oss.get_token()
    return Response(token, status=status.HTTP_200_OK)