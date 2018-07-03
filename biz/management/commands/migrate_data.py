import re
import requests
from io import BytesIO
from json import loads
import secrets
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db.utils import IntegrityError
from django.utils.timezone import get_default_timezone
from django.contrib.auth.hashers import make_password
from biz.services.file_service import generate_file_name, storage
from old_boxing.models import User as OldUser, Article, ArticleComment
from biz.models import User, UserProfile, GameNews, Comment
from biz.constants import USER_IDENTITY_DICT
from biz.redis_client import follow_user
from biz.utils import hans_to_initial
from celery import shared_task

city_dict = {}
with open('old_boxing/citys.txt', 'rb') as fp:
    for i in loads(fp.read().decode('utf-8')):
        city_dict[i['id']] = i['name']

resource_base_url = 'http://boxing-1251438677.cossh.myqcloud.com'

re_resource_base_url = re.compile('\'?\"?(http:\/\/boxing-1251438677\.cossh\.myqcloud\.com.*?)\'?\"\s')

http_client = requests.Session()

PHONE_DICT = {
    10: 16619770891,  # '热门视频'
    11: 15210750150,  # 'Friday'
    12: 15801087215,  # '拳城出击'
    13: 13800138000,  # '客服账号'

    14: 13261843166,  # '跑酷',
    15: 17611655266,  # '熊呈呈',
    16: 13501224847,  # '徐晓冬',
    17: 13810578320,  # '吴紫龙',
    18: 18888888888,  # '拳城出击——中华武术大会',
}

PRESET_PHONE_LIST = PHONE_DICT.values()
PRESET_ID_LIST = PHONE_DICT.keys()

NAME_DICT = {
    10: '热门视频',
    11: 'Friday',
    12: '拳城出击',
    13: '客服账号',

    14: '跑酷',
    15: '熊呈呈',
    16: '徐晓冬',
    17: '吴紫龙',
    18: '拳城出击——中华武术大会',
}
DEFAULT_PASSWORD = '1qaz1qaz1qaZ'


def move_image(url: str):
    if not url:
        return
    if not url.startswith('http'):
        if not url.startswith('/'):
            url = f'/{url}'
        url = f'{resource_base_url}{url}'
    res = http_client.get(url)
    if res.status_code == 200:
        f = File(BytesIO(res.content), url.split('/')[-1])
        file_path = generate_file_name(f)
        url_path = f'{settings.OSS_BASE_URL}{settings.UPLOAD_URL_PATH}{file_path}'
        if http_client.head(url_path).status_code == 200:
            return f'{settings.UPLOAD_URL_PATH}{file_path}'
        return storage.save(file_path, f)


important_user_fields = (
    'phone',
    'nickname',
    'gender',
    'birthday',
    'signature',
    'city',
    'avatar',
    'uicon',
    'uuid',
)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def move_user_worker(uid):
    u = OldUser.objects.get(uid=uid)
    valid_fields = 0
    for field in important_user_fields:
        if getattr(u, field):
            valid_fields += 1
    if valid_fields < 3:
        return

    if not u.phone:
        u.phone = f'{uid}'.rjust(11, '0')

    weibo_openid = wechat_openid = None

    if u.source == 2:
        wechat_openid = u.uuid
    if u.source == 3:
        weibo_openid = u.uuid

    [follow_user(uid, user_id) for user_id in PRESET_ID_LIST]

    new_user, created = User.objects.get_or_create(
        id=uid,
        defaults=dict(
            mobile=u.phone,
            password=f'boxing${u.salt}${u.pass_field}',
            weibo_openid=weibo_openid,
            wechat_openid=wechat_openid,
            is_active=not u.isdel,
            date_joined=u.createtime.replace(tzinfo=get_default_timezone()),
        )
    )
    if not UserProfile.objects.filter(user_id=new_user.id).exists():
        nick_name_index_letter = hans_to_initial(u.nickname)
        avatar = move_image(u.avatar or u.uicon)
        UserProfile.objects.create(
            user_id=uid,
            nick_name=u.nickname[:30] if u.nickname else None,
            nick_name_index_letter=nick_name_index_letter if re.match(r"[a-zA-Z]", nick_name_index_letter) else "#",
            gender=1 if u.gender != 2 else 0,
            birthday=u.birthday,
            bio=u.signature,
            address=city_dict.get(u.city),
            avatar=avatar,
        )


def move_user():
    for u in OldUser.objects.all().order_by('-uid').only('uid', 'phone'):
        if u.phone not in PRESET_PHONE_LIST:
            move_user_worker.delay(u.uid)


def set_preset_user():
    for user_id, phone in PHONE_DICT.items():
        User.objects.get_or_create(
            id=user_id,
            defaults=dict(
                mobile=phone,
                password=make_password(DEFAULT_PASSWORD, secrets.token_hex(32), 'boxing'),
                is_staff=user_id in USER_IDENTITY_DICT.values(),
            )
        )
        nick_name = NAME_DICT[user_id]
        nick_name_index_letter = hans_to_initial(nick_name)
        nick_name_index_letter = nick_name_index_letter if re.match(r"[a-zA-Z]", nick_name_index_letter) else "#"
        UserProfile.objects.get_or_create(
            user_id=user_id,
            defaults=dict(
                nick_name=nick_name,
                nick_name_index_letter=nick_name_index_letter,
            )
        )


def replace_article_img(html):
    for url in re_resource_base_url.findall(html):
        new_url = move_image(url)
        html = html.replace(url, new_url, 1)
    return html


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def fix_news_content_worker(id):
    news = GameNews.objects.get(id=id)
    article = Article.objects.get(id=id)
    news.app_content = replace_article_img(article.contenthtml)
    news.save()


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def move_article_worker(article_id):
    try:
        article = Article.objects.get(id=article_id)
        createtime = article.createtime.replace(tzinfo=get_default_timezone())
        GameNews.objects.get_or_create(
            id=article.id,
            defaults=dict(
                title=article.title[:50],
                sub_title=article.subtitle[:50],
                # operator_id=BOXING_USER_ID,
                views_count=article.realreadnum,
                initial_views_count=article.basereadnum,
                picture=move_image(article.cover),
                stay_top=article.istotop,
                app_content=replace_article_img(article.contenthtml),
                created_time=createtime,
                updated_time=article.updatetime.replace(
                    tzinfo=get_default_timezone()) if article.updatetime else createtime,
                push_news=article.is_push,
                start_time=article.push_start_time.replace(
                    tzinfo=get_default_timezone()) if article.push_start_time else None,
                end_time=article.push_end_time.replace(
                    tzinfo=get_default_timezone()) if article.push_end_time else None,
            )
        )
    except IntegrityError as e:
        print(article_id, e)


def move_article():
    for article in Article.objects.filter(contenttype=1, isdel=0).only('id').order_by('id'):
        move_article_worker.delay(article.id)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3})
def move_comment_worker(comment_id):
    comment = ArticleComment.objects.get(id=comment_id)
    news = GameNews.objects.filter(id=comment.aid).first()
    if news:
        try:
            Comment.objects.get_or_create(
                id=comment.id,
                defaults=dict(
                    content_object=news,
                    content=comment.content,
                    user_id=comment.uid,
                    is_deleted=not comment.isdel,
                    created_time=comment.createtime.replace(tzinfo=get_default_timezone()),
                )
            )
        except IntegrityError as e:
            print(comment.id, comment.uid, e)


def move_comment():
    for c in ArticleComment.objects.filter(isdel=1).only('id'):
        move_comment_worker.delay(c.id)


def fix_news_content():
    for i in GameNews.objects.filter(app_content__contains='https://api.bitu').filter(app_content__contains='video'):
        fix_news_content_worker.delay(i.id)


class Command(BaseCommand):
    help = '迁移数据'

    def handle(self, *args, **options):
        # set_preset_user()
        # move_user()
        # move_article()
        # move_comment()
        fix_news_content()
