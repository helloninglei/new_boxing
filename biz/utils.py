# coding=utf-8
from django.conf import settings
from biz import models
from biz.constants import DEVICE_PLATFORM_IOS, DEVICE_PLATFORM_ANDROID

oss_base_url = settings.OSS_CONFIG['url']


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_device_platform(request):
    value = request.META.get('source', '').lower()
    if value == 'android':
        return DEVICE_PLATFORM_ANDROID
    if value == 'ios':
        return DEVICE_PLATFORM_IOS


def get_model_class_by_name(name):
    return getattr(models, name.title().replace('_', ''))


def get_share_img_url(url, is_video=False):
    if url:
        if is_video:
            return f'{oss_base_url}{url}?x-oss-process=video/snapshot,t_10000,f_jpg,w_120,h_120,m_fast'
        return f'{oss_base_url}{url}?x-oss-process=image/resize,w_120,h_120'

