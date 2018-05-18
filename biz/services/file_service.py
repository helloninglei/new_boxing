# coding: utf-8
import os
import oss2
import hashlib
from urllib.parse import urljoin
from django.conf import settings


class OssClient(object):
    def __init__(self, base_url=None):
        cfg = settings.OSS_CONFIG
        self.base_url = base_url
        self.auth = oss2.Auth(cfg['app_key'], cfg['app_secret'])
        self.bucket = oss2.Bucket(self.auth, cfg['url'], cfg['bucket'])

    def save(self, file_path, file_data):
        file_path = urljoin(self.base_url, file_path)
        self.bucket.put_object(file_path[1:], file_data)
        return file_path


storage = OssClient(base_url=settings.UPLOAD_URL_PATH)


def save_upload_file(upload_file):
    file_path = generate_file_name(upload_file)
    return storage.save(file_path, upload_file)


def generate_file_name(f):
    h = hashlib.sha1()
    while True:
        block = f.read(128 * 1024)
        if not block:
            break
        h.update(block)
    digest = h.hexdigest()
    f.seek(0)
    file_name, file_ext = os.path.splitext(f.name)
    return digest[:2] + '/' + digest[2:4] + '/' + digest[4:] + file_ext
