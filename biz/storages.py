# coding: utf-8
import oss2
from django.conf import settings
from django.core.files.storage import FileSystemStorage


class OssClient(object):
    def __init__(self, base_url=None):
        cfg = settings.OSS_CONFIG
        self.base_url = base_url
        self.auth = oss2.Auth(cfg['app_key'], cfg['app_secret'])
        self.bucket = oss2.Bucket(self.auth, cfg['url'], cfg['bucket'])

    def save(self, file_path, file_data):
        self.bucket.put_object(file_path, file_data)
        return file_path


if settings.ENVIRONMENT == settings.PRODUCTION:
    storage = OssClient(base_url=settings.BASE_UPLOAD_FILE_URL)
else:
    storage = FileSystemStorage(location=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR,
                                base_url=settings.BASE_UPLOAD_FILE_URL)
