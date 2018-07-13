from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.response import Response
from biz.easemob_client import EaseMobClient
from biz.models import WordFilter


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def chat_rooms_info(request):
    sensitive_word_list = WordFilter.objects.values_list("sensitive_word", flat=True)
    chat_rooms_info = EaseMobClient.get_chatrooms()
    return Response({"chat_rooms_info": chat_rooms_info, "sensitive_word_list": sensitive_word_list},
                    status=status.HTTP_200_OK)
