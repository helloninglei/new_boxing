import subprocess as sp
import json
from rest_framework.response import Response
from rest_framework import status
from biz.redis_client import redis_client
from urllib.parse import urlparse
import re

from django.http import StreamingHttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes

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
    pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10 ** 8)
    pipe.wait()
    if pipe.returncode is not 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return StreamingHttpResponse(pipe.stdout, content_type="image/jpeg")


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
        return Response({"height": data['height'], "width": data['width']})

    pipe = sp.Popen(
        ["ffprobe", "-v", "error", "-of", "flat=s=_", "-select_streams", "v:0", "-show_entries", "stream=height,width",
         f"{video_url}"], stdout=sp.PIPE)
    pipe.wait()
    if pipe.returncode is not 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    std_out = pipe.communicate()[0]

    rex = re.compile(r"[^=]*=(\d+)[^=]*=(\d+).*")

    width, height = rex.match(str(std_out)).groups()
    data = {"height": height, "width": width}
    redis_client.hset(VIDEO_RESOLUTION, video_path, json.dumps(data))
    return Response(data)