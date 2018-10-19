from urllib.parse import urlparse

from django.conf import settings


def get_path(url):
    return urlparse(url).path if url.startswith("http") else url


def get_cdn_url(url):
    return f"{settings.CDN_BASE_URL}{get_path(url)}"
