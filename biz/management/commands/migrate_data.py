import requests
from io import BytesIO
from json import load
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from biz.services.file_service import save_upload_file
from old_boxing.models import User as OldUser, UserInfo, Article, ArticleComment, UserReadArticle
from biz.models import User, UserProfile, BoxerIdentification, GameNews

city_dict = {}
with open('old_boxing/citys.txt', 'r') as fp:
    for i in load(fp):
        city_dict[i['id']] = i['name']

resource_base_url = 'http://boxing-1251438677.cossh.myqcloud.com'

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


important_fields = (
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


def move_user():
    for u in OldUser.objects.all().order_by('-uid'):
        valid_fields = 0
        for field in important_fields:
            if getattr(u, field):
                valid_fields += 1
        if valid_fields < 3:
            continue

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
                password=f'{u.pass_field}:{u.salt}',
                weibo_openid=weibo_openid,
                wechat_openid=wechat_openid,
                is_active=not u.isdel,
                date_joined=u.createtime,
            )
        )
        if not UserProfile.objects.filter(user_id=u.uid).exists():
            print(u.avatar)
            print(u.uicon)
            print(u.uid)
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


class Command(BaseCommand):
    help = '迁移数据'

    def handle(self, *args, **options):
        move_user()
