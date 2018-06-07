# coding=utf-8
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.response import Response
from biz.models import Message, HotVideo, GameNews
from biz.redis_client import incr_number_of_share
from biz.utils import get_model_class_by_name, get_share_img_url

'''
带图片（头像）、主标题（取动态文字）、副标题为 “来自xx的拳民出击”，xx为用户昵称。
主标题最多2行展示，文字过多时，以...结束。
如只有图片、视频，主标题默认为“分享XX动态“。XX为用户昵称。



如视频已付费，分享出去还是未付费的分享页。视频是不完整视频。
击xx元观看完整视频”按钮和“打开app”相同，ios打开appstore页。安卓打开下载提示页。“
热门视频分享，主标题 ：视频名称、图片 展示图片 ，副标题 拳民出击。



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
    if isinstance(obj, Message):
        user = obj.user
        title = obj.content
        if hasattr(user, 'user_profile'):
            profile = user.user_profile
            if not title:
                title = f'分享{profile.nick_name}动态'
            sub_title = f'来自{profile.nick_name}的拳民出击'
            picture = get_share_img_url(profile.avatar)
    elif isinstance(obj, HotVideo):
        user = obj.user
        title = obj.name
        sub_title = '拳民出击'
        picture = get_share_img_url(obj.try_url, is_video=True)
    elif isinstance(obj, GameNews):
        title = obj.title
        sub_title = obj.sub_title
        picture = get_share_img_url(obj.picture)
        user = obj.operator
    else:  # course order  TODO 等待course order 重构
        title = obj.course_name
        sub_title = ''
        picture = ''
        user = obj.boxer.user_id

    plural_prefix = 's' if object_type != 'game_news' else ''
    data = {
        'title': _truncate_text(title, 14),
        'sub_title': _truncate_text(sub_title, 20),
        'picture': picture,
        'url': f'{h5_base_url}{object_type}{plural_prefix}/{object_id}',
    }
    incr_number_of_share(user.id)
    return Response(data)
