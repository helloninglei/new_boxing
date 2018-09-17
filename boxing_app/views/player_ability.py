# -*- coding:utf-8 -*-
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from biz.services.chart_service import make_radar
from rest_framework.response import Response
from biz.models import Player, Match
from django.db.models import Q
from biz.constants import SCHEDULE_STATUS_PUBLISHED, MATCH_RESULT_RED_KO_BLUE, MATCH_RESULT_BLUE_KO_RED, \
    MATCH_RESULT_BLUE_SUCCESS, MATCH_RESULT_RED_SUCCESS


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def ability_chart(request, pk):
    player = Player.objects.filter(user_id=pk).first()
    if player:
        ret = make_radar(skill=player.skill, strength=player.strength,
                         defence=player.defence, willpower=player.willpower,
                         attack=player.attack, stamina=player.stamina)
        return StreamingHttpResponse(ret, content_type="image/png")
    return HttpResponse(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def ability_details(request, pk):
    player = Player.objects.filter(user_id=pk).first()
    if player:
        return Response(data={'skill': player.skill, 'strength': player.strength, 'defence': player.defence,
                              'willpower': player.willpower, 'attack': player.attack, 'stamina': player.stamina})
    return Response(status=status.HTTP_404_NOT_FOUND)


def get_ko_er(result):
    if result == MATCH_RESULT_RED_KO_BLUE:
        return 'red'
    elif result == MATCH_RESULT_BLUE_KO_RED:
        return 'blue'
    else:
        return ''


def get_winner(result):
    if result in (MATCH_RESULT_RED_SUCCESS, MATCH_RESULT_RED_KO_BLUE):
        return 'red'
    elif result in (MATCH_RESULT_BLUE_SUCCESS, MATCH_RESULT_BLUE_KO_RED):
        return 'blue'


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def player_match(request, pk):
    player = Player.objects.filter(user_id=int(pk)).first()
    win = 0
    ko = 0
    results = []
    res = {'total': 0, 'win': 0, 'ko': 0, 'results': []}

    if player:
        match_qs = Match.objects.filter(Q(red_player=player) | Q(blue_player=player), schedule__status=SCHEDULE_STATUS_PUBLISHED)
        for m in match_qs:
            record = {}
            record['red_player'] = m.red_player.user.id
            record['red_avatar'] = m.red_player.avatar
            record['red_name'] = m.red_player.name
            record['blue_player'] = m.blue_player.user.id
            record['blue_avatar'] = m.blue_player.avatar
            record['blue_name'] = m.blue_player.name
            record['schedule'] = m.schedule.name
            record['category'] = m.get_category_display()
            record['level_min'] = m.level_min
            record['level_max'] = m.level_max
            record['time'] = m.created_time.strftime('%Y-%m-%d')
            record['ko'] = get_ko_er(m.result)
            record['win'] = get_winner(m.result)
            if int(pk) == record['red_player'] and m.result == MATCH_RESULT_RED_KO_BLUE:
                ko += 1
            if int(pk) == record['blue_player'] and m.result == MATCH_RESULT_BLUE_KO_RED:
                ko += 1
            if int(pk) == record['red_player'] and m.result in (MATCH_RESULT_RED_KO_BLUE, MATCH_RESULT_RED_SUCCESS):
                win += 1
            if int(pk) == record['blue_player'] and m.result in (MATCH_RESULT_BLUE_KO_RED, MATCH_RESULT_BLUE_SUCCESS):
                win += 1
            results.append(record)
        res = {'total': len(results), 'win': win, 'ko': ko, 'results': results}

    return Response(data=res, status=status.HTTP_200_OK)
