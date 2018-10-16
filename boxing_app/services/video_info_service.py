import math
import subprocess as sp
import re
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
        video_info = json.loads(redis_client.hget(VIDEO_RESOLUTION, video_path))
        if "size" in video_info or "height" in video_info or "width" in video_info:
            redis_client.hdel(VIDEO_RESOLUTION, video_path)
        else:
            return video_info

    pipe = sp.Popen(
        ["ffprobe", "-v", "error", "-show_entries", "stream_tags=rotate:", "-show_entries", "stream=width,height", "-show_entries", "format=size",
         "-of", "default=noprint_wrappers=1", f"{video_url}"], stdout=sp.PIPE
    )

    pipe.wait()
    if pipe.returncode is not 0:
        return {"video_height": -1, "video_width": -1, "video_size": -1}  # 失败默认结果返回-1
    std_out = pipe.communicate()[0].decode("utf-8")

    width_match = re.findall(r"width=(\d+)", std_out)
    video_width = width_match[0] if width_match else -1

    height_match = re.findall(r"height=(\d+)", std_out)
    video_height = height_match[0] if height_match else -1

    rotate_match = re.findall(r"rotate=(\d+)", std_out)
    video_rotate = rotate_match[0] if rotate_match else 0

    size_match = re.findall(r"size=(\d+)", std_out)
    video_size = int(size_match[0]) / 1024 / 1024 if size_match else -1

    if video_rotate is not 0:
        video_height, video_width = video_width, video_height
 
    data = {"video_height": video_height, "video_width": video_width, "video_size": math.ceil(video_size)}
    redis_client.hset(VIDEO_RESOLUTION, video_path, json.dumps(data))
    return data


def _get_file_oss_url(path: str) -> str:
    oss_url = OSS_CONFIG.get('url')
    oss_bucket = OSS_CONFIG.get('bucket')
    oss_ret = urlparse(oss_url)
    return urljoin(oss_ret.scheme + "://" + oss_bucket + "." + oss_ret.netloc, path)
