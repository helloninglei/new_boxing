import re
import requests
from io import BytesIO
from json import loads
import secrets
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db.utils import IntegrityError
from django.utils.timezone import get_default_timezone
from django.contrib.auth.hashers import make_password
from biz.services.file_service import save_upload_file
from old_boxing.models import User as OldUser, UserInfo, Article, ArticleComment
from biz.models import User, UserProfile, BoxerIdentification, GameNews, Comment
from biz.constants import FRIDAY_USER_ID, BOXING_USER_ID, HOT_VIDEO_USER_ID, FAMOUS_USER_DICT, USER_IDENTITY_DICT
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


def move_image(url: str):
    if not url:
        return
    if not url.startswith('http'):
        if not url.startswith('/'):
            url = f'/{url}'
        url = f'{resource_base_url}{url}'
    res = http_client.get(url)
    if res.status_code == 200:
        f = File(BytesIO(res.content), 'avatar.jpg')
        return save_upload_file(f)


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
        u.phone = f'{u.uid}'.rjust(11, '0')

    weibo_openid = wechat_openid = None

    if u.source == 2:
        wechat_openid = u.uuid
    if u.source == 3:
        weibo_openid = u.uuid

    new_user, created = User.objects.get_or_create(
        mobile=u.phone,
        defaults=dict(
            id=u.uid,
            password=f'boxing${u.pass_field}${u.salt}',
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
            user_id=u.uid,
            nick_name=u.nickname[:30] if u.nickname else None,
            nick_name_index_letter=nick_name_index_letter if re.match(r"[a-zA-Z]", nick_name_index_letter) else "#",
            gender=1 if u.gender != 2 else 0,
            birthday=u.birthday,
            bio=u.signature,
            address=city_dict.get(u.city),
            avatar=avatar,
        )
    if not BoxerIdentification.objects.filter(user_id=new_user.id).exists():
        u = UserInfo.objects.filter(uid=u.uid).first()
        if u:
            BoxerIdentification.objects.create(
                id=new_user.id,
                user_id=new_user.id,
                real_name=u.name,
                identity_number=u.idcard,
                height=u.stature,
                weight=u.weight,
                job=u.occupation,
                club=u.club,
                is_professional_boxer=u.playertype == 2,
                created_time=u.createtime,
                updated_time=u.updatetime,
                birthday=u.birthday,
            )


def move_user():
    for u in OldUser.objects.all().order_by('-uid').only('uid'):
        move_user_worker.delay(u.uid)


#
# 拳城出击账号： 15801087215 密码：1qaz1qaz1qaZ
# friday账号： 15210750150 密码：1qaz1qaz1qaZ
# app客服账号： 16619770891 密码：1qaz1qaz1qaZ


OFFICIAL_USERS = {
    15801087215: '拳城出击',
    15210750150: 'Friday',
    16619770891: '热门视频',
    13800138000: '客服账号',
}

FAMOUS_USER_NAME_DICT = {
    13261843166: '跑酷',
    17611655266: '熊呈呈',
    13501224847: '徐晓冬',
    13810578320: '吴紫龙',
}

DEFAULT_PASSWORD = '1qaz1qaz1qaZ'


def set_famous_user():
    for phone, user_id in FAMOUS_USER_DICT.items():
        User.objects.get_or_create(
            id=user_id,
            defaults=dict(
                mobile=phone,
                password=make_password(DEFAULT_PASSWORD, secrets.token_hex(32), 'boxing')
            )
        )
        nick_name = FAMOUS_USER_NAME_DICT[phone]
        nick_name_index_letter = hans_to_initial(nick_name)
        nick_name_index_letter = nick_name_index_letter if re.match(r"[a-zA-Z]", nick_name_index_letter) else "#"
        UserProfile.objects.get_or_create(
            user_id=user_id,
            defaults=dict(
                nick_name=nick_name,
                nick_name_index_letter=nick_name_index_letter,
            )
        )


def set_admin_user():
    for mobile in OFFICIAL_USERS.keys():
        u, _ = User.objects.get_or_create(
            mobile=mobile,
        )
        u.set_password(DEFAULT_PASSWORD)
        u.is_staff = True
        u.save()
        profile, _ = UserProfile.objects.get_or_create(
            user_id=u.id,
            defaults=dict(
                nick_name=OFFICIAL_USERS[mobile]
            )
        )


boxing_user = None


def replace_article_img(html):
    for url in re_resource_base_url.findall(html):
        new_url = move_image(url)
        html = html.replace(url, new_url, 1)
    return html


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
                operator=boxing_user,
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
    global boxing_user
    boxing_user = User.objects.get(mobile=15801087215)
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


def follow_official_user():
    for u in User.objects.only('id'):
        [follow_user(u.id, i) for i in USER_IDENTITY_DICT.values()]
        [follow_user(u.id, i) for i in FAMOUS_USER_DICT.values()]


class Command(BaseCommand):
    help = '迁移数据'

    def handle(self, *args, **options):
        set_famous_user()
        move_user()
        set_admin_user()
        follow_official_user()
        # move_article()
        # move_comment()
