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


def move_image(path):
    fdata = http_client.get(f'{resource_base_url}{path}').content
    f = File(BytesIO(fdata), 'avatar.jpg')
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
    # users = []
    for u in OldUser.objects.all():
        valid_fields = 0
        for field in important_fields:
            if getattr(u, field):
                valid_fields += 1
        if not u.phone or valid_fields < 3:
            continue

        weibo_openid = wechat_openid = None

        if u.source == 2:
            wechat_openid = u.uuid
        if u.source == 3:
            weibo_openid = u.uuid

        obj, created = User.objects.get_or_create(
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
            if u.avatar:
                avatar = move_image(u.avatar)
            else:
                avatar = u.uicon
            print(avatar)
            UserProfile.objects.create(
                user_id=u.uid,
                defaults=dict(
                    nick_name=u.nickname,
                    gender=1 if u.gender != 2 else 0,
                    birthday=u.birthday,
                    bio=u.signature,
                    address=city_dict.get(u.city),
                    avatar=avatar,
                )
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
