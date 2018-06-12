from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from biz.constants import USER_IDENTITY_DICT


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def get_official_accounts_info(request):
    return Response({"results": USER_IDENTITY_DICT}, status=status.HTTP_200_OK)
