from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response

from biz.models import BoxingClub


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def get_boxer_list(request):
    """
    拳手城市列表
    """
    city_list = list(BoxingClub.objects.filter(course__is_open=True)
                     .values_list('city_index_letter', 'city')
                     .order_by('city_index_letter'))
    return Response(city_list)
