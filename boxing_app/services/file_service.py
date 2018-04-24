import datetime
import os
import uuid

from boxing_app.serializers import UploadFileSerializer
from biz.storages import storage


def save_upload_file(upfile, user):
    url = _save_upload_file(upfile)
    serializer = UploadFileSerializer(data={
        'origin_name': upfile.name,
        'file_url': url,
        'create_user': user.id,
        'create_time': datetime.datetime.now()
    })
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return url


def _save_upload_file(f):
    file_path = _rename(f)
    return storage.base_url + storage.save(file_path, f)


def only_save_upload_file(f, file_path=None):
    if file_path is None:
        file_path = _rename(f)
    return storage.base_url + storage.save(file_path, f)


def _rename(f):
    fn = uuid.uuid4().hex
    file_name, file_ext = os.path.splitext(f.name)
    year = str(datetime.datetime.today().year)
    file_path = year + '/' + fn[0] + '/' + fn[0:2] + '/' + fn + file_ext
    return file_path
