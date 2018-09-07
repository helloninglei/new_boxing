# coding=utf-8
from time import mktime
from APISender import APISender
from django.conf import settings
from base.APIConstants import Constants
from base.APIMessage import PushMessage
from biz.constants import APP_JUMP_OBEJCT_NEWS, APP_JUMP_OBEJCT_HOT_VIDEO

if settings.ENVIRONMENT == settings.PRODUCTION:
    Constants.use_official()
else:
    Constants.use_sandbox()

android_sender = APISender(settings.XIAOMI_PUSH_APP_SECRET_ANDROID)
ios_sender = APISender(settings.XIAOMI_PUSH_APP_SECRET_IOS)


def broadcast_news(news):
    return broadcast_message(news.title, f'{APP_JUMP_OBEJCT_NEWS}:{news.id}', start_time=news.start_time,
                             end_time=news.end_time)


def broadcast_hot_video(hot_video):
    return broadcast_message(hot_video.name, f'{APP_JUMP_OBEJCT_HOT_VIDEO}:{hot_video.id}', start_time=hot_video.start_time,
                             end_time=hot_video.end_time)


def push_message(mobile, content, jump_to=None, start_time=None, end_time=None):
    user_alias = mobile

    android_msg = _build_message(content, jump_to, start_time, end_time, 'android')
    android_sender.send_to_alias(android_msg.message_dict(), user_alias)

    ios_msg = _build_message(content, jump_to, start_time, end_time, 'ios')
    ios_sender.send_to_alias(ios_msg.message_dict_ios(), user_alias)


def broadcast_message(content, jump_to=None, start_time=None, end_time=None):
    android_msg = _build_message(content, jump_to, start_time, end_time, 'android')
    android_sender.broadcast_all(android_msg.message_dict())

    ios_msg = _build_message(content, jump_to, start_time, end_time, 'ios')
    ios_sender.broadcast_all(ios_msg.message_dict_ios())


def _build_message(content, jump_to, start_time, end_time, device):
    msg = PushMessage().title('拳城出击').description(content).extra({'jump_to': jump_to}).restricted_package_name(
        settings.ANDROID_PACKAGE_NAME)
    if device == 'android':
        msg.payload(content).notify_type(1)
    else:
        msg.restricted_package_name(
            settings.IOS_PACKAGE_NAME)
    if start_time:
        msg.time_to_send(int(mktime(start_time.timetuple())) * 1000)
    if end_time:
        msg.time_to_live((end_time - start_time).microseconds)
    return msg
