import math
import subprocess as sp
import json
import settings
from biz.redis_client import redis_client
from urllib.parse import urlparse, urljoin

from settings import OSS_CONFIG

FFMPEG_BIN = "ffmpeg"
VIDEO_RESOLUTION = "video_resolution"


def video_resolution(video_path: str) -> dict:
    video_url = _get_file_oss_url(video_path)
    if redis_client.hexists(VIDEO_RESOLUTION, video_path):
        return json.loads(redis_client.hget(VIDEO_RESOLUTION, video_path))

    pipe = sp.Popen(
        ["ffprobe", "-v", "error", "-show_entries", "stream=width,height", "-show_entries", "format=size",
         "-of", "json", "-i", f"{video_url}"], stdout=sp.PIPE
    )

    pipe.wait()
    if pipe.returncode is not 0:
        return {"video_height": -1, "video_width": -1, "video_size": -1}  # 失败默认结果返回-1

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
    std_out = pipe.communicate()[0]

    height, width = 0, 0
    video_info = json.loads(std_out.decode("utf-8"))
    for info in video_info['streams']:
        if info.get("height") and info.get("width"):
            width = info.get("width")
            height = info.get("height")
            break

    size = int(video_info['format']['size']) / 1024 / 1024
    data = {"video_height": height, "video_width": width, "video_size": math.ceil(size)}
    redis_client.hset(VIDEO_RESOLUTION, video_path, json.dumps(data))
    return data


def _get_file_oss_url(path: str) -> str:
    oss_url = OSS_CONFIG.get('url')
    oss_bucket = OSS_CONFIG.get('bucket')
    oss_ret = urlparse(oss_url)
    return urljoin(oss_ret.scheme + "://" + oss_bucket + "." + oss_ret.netloc, path)
