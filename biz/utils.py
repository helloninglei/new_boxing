# coding=utf-8
from biz.constants import DEVICE_PLATFORM_IOS, DEVICE_PLATFORM_ANDROID


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

