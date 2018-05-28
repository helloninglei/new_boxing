"""boxing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""

from django.urls import include, path, re_path
from django.conf import settings
from biz.views import upload_file
from boxing_app.views.boxer import BoxerIdentificationViewSet
from boxing_app.views import message
from boxing_app.views import comment
from boxing_app.views import report
from boxing_app.views import like
from boxing_app.views import follow
from boxing_app.views.course import BoxerMyCourseViewSet
from boxing_app.views.orders import BoxerCourseOrderViewSet, UserCourseOrderViewSet, CourseOrderCommentViewSet
from boxing_app.views.verify_code import send_verify_code
from biz.constants import REPORT_OBJECT_DICT, COMMENT_OBJECT_DICT, PAYMENT_OBJECT_DICT, SHARE_OBJECT_DICT, \
    USER_IDENTITY_DICT
from boxing_app.views import register
from boxing_app.views import login
from biz.views import captcha_image
from boxing_app.views.user_profile import UserProfileViewSet, BlackListViewSet
from boxing_app.views.hot_video import HotVideoViewSet
from boxing_app.views import pay
from boxing_app.views import game_news
from boxing_app.views.banner import BannerViewSet
from boxing_app.views.wallet import MoneyChangeLogViewSet, money_balance
from boxing_app.views.share import share_view
from boxing_app.views.user_profile import bind_alipay_account, user_profile_redirect
from boxing_app.views.wallet import WithdrawViewSet

boxer_identification = BoxerIdentificationViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'retrieve'})

discover_urls = [
    path('messages', message.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-latest'),
    path('messages/hot', message.MessageViewSet.as_view({'get': 'hot'}), name='message-hot'),
    path('messages/mine', message.MessageViewSet.as_view({'get': 'mine'}), name='message-mine'),
    path('messages/following', message.MessageViewSet.as_view({'get': 'following'}), name='message-following'),
    path('messages/<int:pk>', message.MessageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}),
         name='message-detail'),
    path('messages/<int:message_id>/like',
         like.LikeViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='messgae-like'),
]

comment_object_string = '|'.join(COMMENT_OBJECT_DICT.keys())
comment_urls = [
    re_path(r'^(?P<object_type>({0}))s?/(?P<object_id>\d+)/comments$'.format(comment_object_string),
            comment.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    re_path(r'^(?P<object_type>({0}))s?/(?P<object_id>\d+)/comments/(?P<pk>\d+)$'.format(comment_object_string),
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
]

course_url = [
    path('boxer/course', BoxerMyCourseViewSet.as_view({'get': 'list', 'post': 'update'})),
]

order_url = [
    path('boxer/orders', BoxerCourseOrderViewSet.as_view({'get': 'list'}), name='boxer-orders'),
    path('boxer/order/<int:pk>', BoxerCourseOrderViewSet.as_view({'get': 'retrieve'}), name='boxer-order-detail'),
    path('user/orders', UserCourseOrderViewSet.as_view({'get': 'list'}), name='user-orders'),
    path('user/order/<int:pk>', UserCourseOrderViewSet.as_view({'get': 'retrieve'}), name='user-order-detail')
]

order_comment_url = [
    path('course/order/<int:order_id>/comment', CourseOrderCommentViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('course/order/<int:order_id>/comment/<int:pk>', CourseOrderCommentViewSet.as_view({'get': 'retrieve'})),
]

follow_url = [
    path('follow', follow.BaseFollowView.as_view()),
    path('follower', follow.FollowerView.as_view()),
    path('follower/<int:user_id>', follow.FollowerView.as_view()),
    path('following', follow.FollowingView.as_view()),
    path('following/<int:user_id>', follow.FollowingView.as_view()),
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
    path("register_with_user_info", register.register_with_user_info),
    path("mobile/change", register.change_mobile)
]

login_urls = [
    path("login_is_need_captcha", login.login_is_need_captcha),
    re_path(r"^", include("biz.urls")),
    path("password/reset", login.reset_password),
    path("password/change", login.change_password)
]


official_user_string = '|'.join(USER_IDENTITY_DICT.keys())
user_urls = [
    path("alipay_account", bind_alipay_account),
    path("user_profile", UserProfileViewSet.as_view({"get": "retrieve", "put": "update"})),
    path("user_profile/<int:pk>", UserProfileViewSet.as_view({"get": 'retrieve'}), name='user-profile'),
    re_path(r'^user_profile/(?P<user_identity>({0}))'.format(official_user_string), user_profile_redirect),
    path("user_profile_patch", UserProfileViewSet.as_view({"put": "partial_update"})),
    path("black_list", BlackListViewSet.as_view({"get": "list"})),
    path("black_list/<int:pk>", BlackListViewSet.as_view({"get": "retrieve", "delete": "destroy", "post": "create"}))
]

hot_video_url = [
    path('users/<int:user_id>/hot_videos', HotVideoViewSet.as_view({'get': 'list'}), name='hot-video'),
    path('users/<int:user_id>/hot_videos/<int:pk>', HotVideoViewSet.as_view({'get': 'retrieve'}),
         name='hot-video-detail'),
]

payment_object_string = '|'.join(PAYMENT_OBJECT_DICT.keys())
payment_urls = [
    re_path(r'^(?P<object_type>({0}))s/create_order'.format(payment_object_string), pay.create_order,
            name='create-order'),
    re_path(r'^(?P<object_type>({0}))s/create_unpaid_order'.format(payment_object_string), pay.create_unpaid_order,
            name='create-unpaid-order'),
    path('callback/alipay', pay.alipay_calback),
    path('callback/wechat', pay.wechat_calback),
]

news_urls = [
    path('game_news', game_news.NewsViewSet.as_view({'get': 'list'})),
    path('game_news/<int:pk>', game_news.NewsViewSet.as_view({'get': 'retrieve'})),
]

banner_urls = [
    path('banners', BannerViewSet.as_view({'get': 'list'}), name='banner-list'),
]

wallet_urls = [
    path('money_change_log', MoneyChangeLogViewSet.as_view({"get": "list"})),
    path('money_balance', money_balance),
    path("withdraw", WithdrawViewSet.as_view({"post": "create"}))
]

share_object_string = '|'.join(SHARE_OBJECT_DICT.keys())
share_urls = [
    re_path(r'^(?P<object_type>({0}))s?/(?P<object_id>\d+)/share'.format(share_object_string), share_view, name='share'),
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
urlpatterns += payment_urls
urlpatterns += user_urls
urlpatterns += order_url
urlpatterns += course_url
urlpatterns += news_urls
urlpatterns += order_comment_url
urlpatterns += banner_urls
urlpatterns += wallet_urls
urlpatterns += share_urls

if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
