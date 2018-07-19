# coding=utf-8

from django.conf import settings
from pypinyin import pinyin, Style
from rest_framework.exceptions import NotFound
from django.db.models.query import QuerySet
from django.db.models import Count, Q, Func
from biz import models
from biz.constants import DEVICE_PLATFORM_IOS, DEVICE_PLATFORM_ANDROID

oss_base_url = settings.OSS_BASE_URL


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


def get_device_platform(request):
    value = request.META.get('HTTP_SOURCE', '').lower()
    if value == 'android':
        return DEVICE_PLATFORM_ANDROID
    if value == 'ios':
        return DEVICE_PLATFORM_IOS


def get_model_class_by_name(name):
    if name == 'boxer':
        return models.BoxerIdentification
    return getattr(models, name.title().replace('_', ''))


def get_share_img_url(url, is_video=False):
    if url:
        if is_video:
            return f'{oss_base_url}{url}?x-oss-process=video/snapshot,t_10000,f_jpg,w_120,h_120,m_fast'
        if not url.startswith('http'):
            return f'{oss_base_url}{url}?x-oss-process=image/resize,w_120,h_120'
        return url


def get_video_cover_url(url):
    if url:
        return f'{url}?x-oss-process=video/snapshot,t_10000,f_jpg,w_800,m_fast'


def hans_to_initial(hans):
    """返回中文词组第一个汉字的首字母"""
    if not hans:
        return ""
    first_hans = hans[0]
    first_letter = pinyin(first_hans, style=Style.FIRST_LETTER)
    return first_letter[0][0].upper()


def get_object_or_404(queryset, message='数据跑偏了，刷新试试～', **kwargs):
    if not isinstance(queryset, QuerySet):
        queryset = queryset.objects.all()
    queryset = queryset.filter(**kwargs)
    if not queryset.exists():
        raise NotFound(message)
    return queryset.first()


comment_count_condition = Count('comments', filter=Q(comments__is_deleted=False) & (
        Q(comments__ancestor__is_deleted=False) | Q(comments__ancestor__isnull=True)),
                                distinct=True)


class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 1)'
