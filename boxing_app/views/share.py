# coding=utf-8
from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from biz.models import Message, HotVideo, GameNews, UserProfile, User, Player
from biz.redis_client import incr_number_of_share, forward_message, forward_hotvideo, follower_count, following_count
from biz.utils import get_model_class_by_name, get_share_img_url, get_object_or_404
from biz.weixin_public_client import Sign

'''
带图片（头像）、主标题（取动态文字）、副标题为 “来自xx的拳城出击”，xx为用户昵称。
主标题最多2行展示，文字过多时，以...结束。
如只有图片、视频，主标题默认为“分享XX动态“。XX为用户昵称。



如视频已付费，分享出去还是未付费的分享页。视频是不完整视频。
击xx元观看完整视频”按钮和“打开app”相同，ios打开appstore页。安卓打开下载提示页。“
热门视频分享，主标题 ：视频名称、图片 展示图片 ，副标题 拳城出击。



图文资讯-新增资讯/修改 分为 app内正文 和 app外分享正文。
app内正文必填，app外分享正文选填。如未填写app外分享正文，app内和app外分享都显示app内正文。
如有 app外分享正文，则分享后，显示app外分享正文。app内还是显示app内正文。


详情页分享设计规范
https://ad.weixin.qq.com/learn/n6
'''

h5_base_url = settings.SHARE_H5_BASE_URL


def _truncate_text(s, length):
    if len(s) <= length:
        return s
    return f'{s[:length-3]}...'


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
@authentication_classes([])
def share_view(request, object_type, object_id):
    model_class = get_model_class_by_name(object_type)
    obj = get_object_or_404(model_class, pk=object_id)
    sub_title = picture = ''
    plural_prefix = 's' if object_type != 'game_news' else ''
    url = f'{h5_base_url}{object_type}{plural_prefix}/{object_id}'
    weibo = ''  # 微博分享专用字段，解决因产品需求导致分享文案不同问题
    if isinstance(obj, Message):
        user = obj.user
        title = obj.content
        if hasattr(user, 'user_profile'):
            profile = user.user_profile
            if not title:
                title = f'分享{profile.nick_name}动态'
            sub_title = f'来自拳城出击的{profile.nick_name}'
            picture = get_share_img_url(profile.avatar)
        title = _truncate_text(title, 14)
        sub_title = _truncate_text(sub_title, 20)
        forward_message(object_id)
    elif isinstance(obj, HotVideo):
        user_id = request.GET.get('user_id')
        if user_id:
            user = get_object_or_404(User, pk=user_id)
        else:
            user = obj.users.first()
        title = obj.name
        sub_title = f'来自拳城出击的热门视频'
        picture = get_share_img_url(obj.cover) or get_share_img_url(obj.try_url, is_video=True)
        url = f'{h5_base_url}hot_videos/{user.id}/{object_id}'
        forward_hotvideo(object_id)
    elif isinstance(obj, GameNews):
        title = obj.title
        sub_title = obj.sub_title
        picture = get_share_img_url(obj.picture)
        user = obj.operator
        url = f'{h5_base_url}game_news/{object_id}/0'  # 0 不在app内打开
    elif isinstance(obj, Player):
        title = f'分享{obj.user.user_profile.nick_name}的个人战绩'
        user = obj.user
        follower = follower_count(user.id)
        following = following_count(user.id)
        sub_title = f'已关注: {following},粉丝数: {follower}'
        picture = get_share_img_url(obj.avatar)
        url = f'{h5_base_url}players/{obj.id}'
        weibo = url + f'  分享来自拳城出击的{user.user_profile.nick_name}的精彩瞬间'
    else:
        title = '我在拳城出击发现了一个很棒的拳击教练，一起去约课吧～'
        sub_title = '上拳城，玩转拳击'
        picture = get_share_img_url(UserProfile.objects.filter(user_id=obj.id).only('avatar').first().avatar)
        user = obj

    data = {
        'title': title,
        'sub_title': sub_title,
        'picture': picture,
        'url': url,
        'weibo': weibo
    }
    if user:
        incr_number_of_share(user.id)
    return Response(data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def second_share_signature(request):
    url = request.query_params.get("url", "")
    return Response(Sign(url).sign())
