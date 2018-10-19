from urllib.parse import urlparse

from django.conf import settings


def get_path(url):
    if url.startswith("http"):
        return urlparse(url).path
    return url


def get_cdn_url(url):
    path = get_path(url)
    return f"{settings.CDN_BASE_URL}{path}"
