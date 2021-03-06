import subprocess as sp
from rest_framework.response import Response
from rest_framework import status
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
    pipe = sp.Popen(args=command, stdout=sp.PIPE)

    image_stream = pipe.communicate()

    if pipe.returncode is not 0:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return StreamingHttpResponse(image_stream, content_type="image/jpeg")
