"""boxing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from biz.views import upload_file
from boxing_app.views.boxer import BoxerIdentificationViewSet, BoxerCourseOrderViewSet
from boxing_app.views import message
from boxing_app.views import comment
from boxing_app.views import report
from boxing_app.views import like
from boxing_app.views import follow
from boxing_app.views.verify_code import send_verify_code
from biz.constants import REPORT_OBJECT_DICT, COMMENT_OBJECT_DICT
from boxing_app.views import register
from boxing_app.views import login
from boxing_app.views.hot_video import HotVideoViewSet, hot_videos_redirect
from biz.views import captcha_image
from boxing_app.views.user_profile import bind_alipay_account

boxer_identification = BoxerIdentificationViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'retrieve'})

discover_urls = [
    path('messages', message.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-latest'),
    path('messages/hot', message.MessageViewSet.as_view({'get': 'hot'}), name='message-hot'),
    path('messages/mine', message.MessageViewSet.as_view({'get': 'mine'}), name='message-mine'),
    path('messages/followed', message.MessageViewSet.as_view({'get': 'followed'}), name='message-followed'),
    path('messages/<int:pk>', message.MessageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='message-detail'),
    path('messages/<int:message_id>/like',
         like.LikeViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='messgae-like'),
]

comment_object_string = '|'.join(COMMENT_OBJECT_DICT.keys())
comment_urls = [
    re_path(r'^(?P<object_type>({0}))s/(?P<object_id>\d+)/comments$'.format(comment_object_string),
            comment.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    re_path(r'^(?P<object_type>({0}))s/(?P<object_id>\d+)/comments/(?P<pk>\d+)$'.format(comment_object_string),
            comment.ReplyViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='comment-detail'),
]

upload_urls = [
    path('upload', upload_file, name='upload'),
]

report_object_string = '|'.join(REPORT_OBJECT_DICT.keys())
report_urls = [
    re_path(r'^(?P<object_type>({0}))s/report$'.format(report_object_string),
            report.ReportViewSet.as_view({'post': 'create'}), name='report'),
    path('report_reason', report.ReportViewSet.as_view({'get': 'retrieve'}), name='report-reason')
]

boxer_url = [
    path('boxer/identification', boxer_identification, name='boxer_identification'),
    path('boxer/course/orders', BoxerCourseOrderViewSet.as_view({'get': 'list'}), name='boxer-course-orders'),
    path('boxer/course/order/<int:pk>', BoxerCourseOrderViewSet.as_view({'get': 'retrieve'}),
         name='boxer-course-order-detail'),
]

follow_url = [
    path('follow', follow.BaseFollowView.as_view()),
    path('follower', follow.FollowerView.as_view()),
    path('followed', follow.FollowedView.as_view()),
    path('unfollow', follow.UnFollowView.as_view()),
]

captcha_urls = [
    re_path('^captcha/', include('captcha.urls')),
    path("captcha-image", captcha_image)
]

verify_code_urls = [
    path("verify_code", send_verify_code)
]

register_urls = [
    path("mobile_register_status", register.mobile_register_status),
    path("is_need_captcha", register.is_need_captcha),
    path("register", register.register),
    path("register_with_user_info", register.register_with_user_info)
]

login_urls = [
    path("login_is_need_captcha", login.login_is_need_captcha),
    re_path(r"^", include("biz.urls")),
    path("password/reset", login.reset_password),
    path("password/change", login.change_password)
]

user_urls = [
    path("alipay_account", bind_alipay_account)
]

hot_video_url = [
    path('users/<int:user_id>/hot_videos', HotVideoViewSet.as_view({'get': 'list'}), name='hot-video'),
    path('hot_videos', hot_videos_redirect),
]

urlpatterns = []
urlpatterns += upload_urls
urlpatterns += boxer_url
urlpatterns += discover_urls
urlpatterns += comment_urls
urlpatterns += report_urls
urlpatterns += follow_url
urlpatterns += captcha_urls
urlpatterns += verify_code_urls
urlpatterns += register_urls
urlpatterns += login_urls
urlpatterns += hot_video_url
urlpatterns += user_urls
if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
    urlpatterns += static(settings.BASE_UPLOAD_FILE_URL, document_root=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR)
