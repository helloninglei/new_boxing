from rest_framework.decorators import api_view
from biz.redis_client import redis_client
from biz.redis_const import UNREAD_COMMENT, UNREAD_LIKE
from rest_framework.response import Response


@api_view(['GET'])
def has_unread_like_and_comment(request):
    return Response(
        {
            "has_unread_like": bool(redis_client.llen(UNREAD_LIKE.format(user_id=request.user.id))),
            "has_unread_comment": bool(redis_client.llen(UNREAD_COMMENT.format(user_id=request.user.id)))
        }
    )
