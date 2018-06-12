from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from biz.constants import USER_IDENTITY_DICT


@api_view(['GET'])
def get_official_accounts_info(request):
    return Response(USER_IDENTITY_DICT, status=status.HTTP_200_OK)
