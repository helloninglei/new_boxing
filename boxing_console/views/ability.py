# -*- coding:utf-8 -*-
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from biz.services.chart_service import make_radar


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def ability_chart(request):
    '''
    :param request:
    eg:
        http://host:port/path?skill=50&strength=80&defence=90&willpower=76&attack=86&stamina=83
    :return:
    '''
    skill = request.GET.get('skill', '')
    strength = request.GET.get('strength', '')
    defence = request.GET.get('defence', '')
    willpower = request.GET.get('willpower', '')
    attack = request.GET.get('attack', '')
    stamina = request.GET.get('stamina', '')

    values = [skill, strength, defence, willpower, attack, stamina]
    if all(map(lambda x: x.isdigit() and 0 < int(x) <= 100, values)):
        result = make_radar(*map(int, values))
        if result:
            return StreamingHttpResponse(result, content_type="image/png", status=status.HTTP_200_OK)

    return HttpResponse(status=status.HTTP_400_BAD_REQUEST)
