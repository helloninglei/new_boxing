# -*- coding:utf-8 -*-
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from biz.services.chart_service import make_radar
from biz.models import Player, Schedule, Match


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def ability_chart(request, pk):
    player = Player.objects.filter(user_id=pk).first()
    if player:
        ret = make_radar(skill=player.skill,  strength=player.strength,
                         defence=player.defence, willpower=player.willpower,
                         attack=player.attack, stamina=player.stamina)
        return StreamingHttpResponse(ret, content_type="image/png")
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)
