# -*- coding:utf-8 -*-
from django.http import StreamingHttpResponse, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from biz.services.chart_service import make_radar
from rest_framework.response import Response
from biz.models import Player, Match, User, UserProfile
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


# 获取ko效果player
def get_ko_player(result):
    if result == MATCH_RESULT_RED_KO_BLUE:
        return 'red'
    elif result == MATCH_RESULT_BLUE_KO_RED:
        return 'blue'
    else:
        return ''


# 获取胜利者
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
    response_data = {'total': 0, 'win': 0, 'ko': 0, 'results': []}

    if player:
        pk = int(pk)
        win = 0
        ko = 0
        results = []
        match_qs = Match.objects.filter(Q(red_player=player) | Q(blue_player=player),
                                        schedule__status=SCHEDULE_STATUS_PUBLISHED).select_related('schedule', 'red_player',
                                                                                                   'blue_player').order_by("-schedule__race_date")
        for match in match_qs:
            record = {}
            record['red_player'] = match.red_player.user.id
            record['red_avatar'] = match.red_player.avatar
            record['red_name'] = match.red_player.name
            record['blue_player'] = match.blue_player.user.id
            record['blue_avatar'] = match.blue_player.avatar
            record['blue_name'] = match.blue_player.name
            record['schedule'] = match.schedule.name
            record['category'] = match.get_category_display()
            record['level_min'] = match.level_min
            record['level_max'] = match.level_max
            record['time'] = match.schedule.race_date
            record['ko'] = get_ko_player(match.result)
            record['win'] = get_winner(match.result)
            # 根据当前用户id判断角色(红方还是蓝方)统计ko场数和总胜利场数
            if pk == record['red_player'] and match.result == MATCH_RESULT_RED_KO_BLUE:
                ko += 1
            if pk == record['blue_player'] and match.result == MATCH_RESULT_BLUE_KO_RED:
                ko += 1
            if pk == record['red_player'] and match.result in (MATCH_RESULT_RED_KO_BLUE, MATCH_RESULT_RED_SUCCESS):
                win += 1
            if pk == record['blue_player'] and match.result in (MATCH_RESULT_BLUE_KO_RED, MATCH_RESULT_BLUE_SUCCESS):
                win += 1
            results.append(record)
        response_data = {'total': len(results), 'win': win, 'ko': ko, 'results': results}

    return Response(data=response_data, status=status.HTTP_200_OK)


# 输入月份和日期，获取星座
def get_constellation(month, date):
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = ("摩羯", "水瓶", "双鱼", "白羊", "金牛", "双子", "巨蟹", "狮子", "处女", "天秤", "天蝎", "射手", "摩羯")
    if date < dates[month - 1]:
        return constellations[month - 1] + '座'
    else:
        return constellations[month] + '座'


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def player_info(request, pk):
    if not Player.objects.filter(user_id=pk).exists():
        return Response(status=404)

    tags = []
    user_profile = UserProfile.objects.filter(user_id=pk).first()
    real_name = user_profile.name
    bio = user_profile.bio
    nick_name = user_profile.user.title
    
    nation = user_profile.nation
    if nation:
        tags.append(nation)
    birthday = user_profile.birthday
    if birthday:
        tags.append(get_constellation(birthday.month, birthday.day))
    address = user_profile.address
    if address:
        tags.append(address)
    height = user_profile.height
    if height:
        tags.append(str(height) + 'cm')
    weight = user_profile.weight
    if weight:
        tags.append(str(weight) + 'kg')
    profession = user_profile.profession
    if profession:
        tags.append(profession)

    data = {'real_name': real_name, 'signature': bio, 'title': nick_name, 'tags': tags}

    return Response(data=data)
