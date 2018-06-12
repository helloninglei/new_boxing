import gevent
import requests
from io import BytesIO
from json import load
from django.core.management.base import BaseCommand
from django.core.files import File
from django.db.utils import IntegrityError
from django.utils.timezone import get_default_timezone
from gevent import queue
from biz.services.file_service import save_upload_file
from old_boxing.models import User as OldUser, UserInfo, Article, ArticleComment
from biz.models import User, UserProfile, BoxerIdentification, GameNews, Comment

city_dict = {}
with open('old_boxing/citys.txt', 'r') as fp:
    for i in load(fp):
        city_dict[i['id']] = i['name']

resource_base_url = 'http://boxing-1251438677.cossh.myqcloud.com'

http_client = requests.Session()

q = queue.Queue(maxsize=20)


def worker():
    while 1:
        try:
            task = q.get(timeout=10)
            func, obj = task
            func(obj)
        except queue.Empty:
            break


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


def move_user_worker(u):
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

    User.objects.get_or_create(
        id=u.uid,
        defaults=dict(
            mobile=u.phone,
            password=f'boxing${u.pass_field}${u.salt}',
            weibo_openid=weibo_openid,
            wechat_openid=wechat_openid,
            is_active=not u.isdel,
            date_joined=u.createtime.replace(tzinfo=get_default_timezone()),
        )
    )
    if not UserProfile.objects.filter(user_id=u.uid).exists():
        avatar = move_image(u.avatar or u.uicon)
        UserProfile.objects.create(
            user_id=u.uid,
            nick_name=u.nickname[:30] if u.nickname else None,
            gender=1 if u.gender != 2 else 0,
            birthday=u.birthday,
            bio=u.signature,
            address=city_dict.get(u.city),
            avatar=avatar,
        )
    if not BoxerIdentification.objects.filter(user_id=u.uid).exists():
        u = UserInfo.objects.filter(uid=u.uid).first()
        if u:
            BoxerIdentification.objects.create(
                id=u.uid,
                user_id=u.uid,
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
    for u in OldUser.objects.all().order_by('-uid'):
        q.put((move_user_worker, u))


#
# 拳城出击账号： 15801087215 密码：1qaz1qaz1qaZ
# friday账号： 15210750150 密码：1qaz1qaz1qaZ
# app客服账号： 16619770891 密码：1qaz1qaz1qaZ


OFFICIAL_USERS = {
    15801087215: '拳城出击',
    15210750150: 'Friday',
    16619770891: '官方客服',
}


def set_admin_user():
    for mobile in OFFICIAL_USERS.keys():
        u, _ = User.objects.get_or_create(
            mobile=mobile,
        )
        u.set_password('1qaz1qaz1qaZ')
        u.is_staff = True
        u.save()
        profile, _ = UserProfile.objects.get_or_create(
            user_id=u.id,
            defaults=dict(
                nick_name=OFFICIAL_USERS[mobile]
            )
        )


boxing_user = None


def move_article_worker(article):
    try:
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
                app_content=article.contenthtml,
                created_time=article.createtime.replace(tzinfo=get_default_timezone()),
                push_news=article.is_push,
                start_time=article.push_start_time.replace(
                    tzinfo=get_default_timezone()) if article.push_start_time else None,
                end_time=article.push_end_time.replace(
                    tzinfo=get_default_timezone()) if article.push_end_time else None,
            )
        )
    except IntegrityError as e:
        print(article.id, e)


def move_article():
    global boxing_user
    boxing_user = User.objects.get(mobile=15801087215)
    for article in Article.objects.filter(contenttype=1, isdel=0).order_by('id'):
        q.put((move_article_worker, article))


def move_comment_worker(comment):
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
    for c in ArticleComment.objects.filter(isdel=1):
        q.put((move_comment_worker, c))


class Command(BaseCommand):
    help = '迁移数据'

    def handle(self, *args, **options):
        workers = [gevent.spawn(worker) for _ in range(20)]
        move_user()
        set_admin_user()
        move_article()
        move_comment()
        gevent.joinall(workers)
