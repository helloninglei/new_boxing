import os
import uuid
import datetime
from biz.storages import storage

def save_upload_file(upfile):
    file_path = _rename(upfile)
    return storage.base_url + storage.save(file_path, upfile)


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
