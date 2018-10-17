import math
import subprocess as sp
import json
from rest_framework.response import Response
from rest_framework import status

import settings
from biz.redis_client import redis_client
from urllib.parse import urlparse, urljoin

from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

from settings import OSS_CONFIG

FFMPEG_BIN = "ffmpeg"
VIDEO_RESOLUTION = "video_resolution"


@api_view(['GET'])
@permission_classes([])
@authentication_classes([])
def cover_picture(request):
    # doc: https://www.ffmpeg.org/ffmpeg.html
    command = [FFMPEG_BIN,
               '-ss', '0',
               "-i", f'{request.query_params.get("video_url")}',
               '-vframes', '1',
               '-vf', 'scale=480:trunc(ow/a/2)*2',
               '-f', 'image2pipe',
               '-']
    pipe = sp.Popen(args=command, stdout=sp.PIPE)
    image_stream = pipe.communicate()
    if pipe.returncode is not 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return StreamingHttpResponse(image_stream, content_type="image/jpeg")


@api_view(['POST'])
@permission_classes([])
@authentication_classes([])
def video_resolution(request):
    video_url = request.data.get('video_url')
    if not video_url:
        return Response(status.HTTP_400_BAD_REQUEST)
    video_path = urlparse(video_url).path
    if redis_client.hexists(VIDEO_RESOLUTION, video_path):
        data = json.loads(redis_client.hget(VIDEO_RESOLUTION, video_path))
        try:
            return Response({"height": data['height'], "width": data['width'], "size": data['size']})
        except KeyError:
            pass
    if settings.ENVIRONMENT != settings.DEVELOPMENT:
        video_url = _get_file_oss_url(video_url)
    pipe = sp.Popen(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-show_entries", "format=size",
         "-of", "json", "-i", f"{video_url}"],
        stdout=sp.PIPE)

    pipe.wait()
    if pipe.returncode is not 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    std_out = pipe.communicate()[0]
    """
    std_out data like this:
    {
        "streams": {
            {
            ...
            "width":960,
            "height":540,
            ...
            },
        }
        "format": {
            ...
            "size":"537296",
            ...
        }
    }
    """
    video_info = json.loads(std_out.decode('utf-8'))
    width, height = 640, 360
    for info in video_info['streams']:
        if info.get('height') and info.get('width'):
            width = info.get('width')
            height = info.get('height')
            break
    size = int(video_info['format']['size']) / 1024 / 1024
    data = {"height": height, "width": width, "size": math.ceil(size)}
    redis_client.hset(VIDEO_RESOLUTION, video_path, json.dumps(data))
    return Response(data)


def _get_file_oss_url(url):
    oss_url = OSS_CONFIG.get('url')
    oss_bucket = OSS_CONFIG.get('bucket')
    origin_ret = urlparse(url)
    oss_ret = urlparse(oss_url)
    return urljoin(origin_ret.scheme + "://" + oss_bucket + "." + oss_ret.netloc, origin_ret.path)
