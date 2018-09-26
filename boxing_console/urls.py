"""boxing_console URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.urls import include, path, re_path
from django.conf import settings

from boxing_console.views.boxer_approve import BoxerIdentificationViewSet
from boxing_console.views.club import BoxingClubVewSet
from boxing_console.views.coin_and_money import CoinChangLogViewSet
from boxing_console.views.course import CourseViewSet, CourseOrderViewSet, CourseSettleOrderViewSet
from boxing_console.views.user_management import UserManagementViewSet
from boxing_console.views.hot_video import HotVideoViewSet, hot_video_user_list, hot_video_tag_list
from boxing_console.views.game_news import NewsViewSet
from boxing_console.views.banner import BannerViewSet
from biz.views import upload_file, captcha_image
from boxing_console.views.financial_management import WithdrawLogViewSet, PayOrdersViewSet
from boxing_console.views import admin, report
from rest_framework.routers import SimpleRouter
from boxing_console.views.user_management import MoneyBalanceChangeLogViewSet, EditUserInfo
from boxing_console.views.official_account_change_logs import OfficialAccountChangeLogsViewSet
from boxing_console.views.message import MessageViewSet
from boxing_console.views.word_filter import WordFilterViewSet
from boxing_console.views.album import AlbumViewSet, AlbumPictureViewSet


router = SimpleRouter()

boxer_url = [
    path('boxer/identification', BoxerIdentificationViewSet.as_view({'get': 'list'}), name='boxer_identification_list'),
    path('boxer/identification/<int:pk>', BoxerIdentificationViewSet.as_view({'get': 'retrieve'}),
         name='boxer_identification_detail'),
    re_path('^boxer/identification/(?P<pk>\d+)/(?P<lock_type>(LOCK|UNLOCK))',
            BoxerIdentificationViewSet.as_view({'post': 'change_lock_state'}), name='change_lock_state'),
    path('boxer/identification/<int:pk>/approve', BoxerIdentificationViewSet.as_view({'post': 'approve'}),
         name='identification_approve'),
    path('boxer/identification/<int:pk>/refuse', BoxerIdentificationViewSet.as_view({'post': 'refuse'}),
         name='identification_refuse'),
]

hot_video_url = [
    path('hot_videos_tags', hot_video_tag_list),
    path('hot_videos', HotVideoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('hot_videos/<int:pk>',
         HotVideoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'})),
    path('hot_videos/users', hot_video_user_list),
]

course_url = [
    path('courses', CourseViewSet.as_view({'get': 'list'}), name='courses_list'),
    path('course/<int:pk>', CourseViewSet.as_view({'get': 'retrieve'}), name='course_detail'),
    path('course/orders', CourseOrderViewSet.as_view({'get': 'list'})),
    path('course/order/<int:pk>', CourseOrderViewSet.as_view({'get': 'retrieve'})),
    path('course/settle_orders', CourseSettleOrderViewSet.as_view({'get': 'list'})),
    path('order/<int:pk>/mark_insurance', CourseOrderViewSet.as_view({'post': 'mark_insurance'}))
]

club_url = [
    path('club', BoxingClubVewSet.as_view({'post': 'create', 'get': 'list'})),
    path('club/<int:pk>', BoxingClubVewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    re_path("^club/(?P<pk>\d+)/(?P<operate>(open|close))$", BoxingClubVewSet.as_view({'post': 'operate'}))
]

login_urls = [
    re_path("^", include("biz.urls"))
]

captcha_urls = [
    re_path('^captcha/', include('captcha.urls')),
    path("captcha-image", captcha_image)
]

upload_url = [
    path('upload', upload_file, name='upload'),
]

news_urls = [
    path('game_news', NewsViewSet.as_view({'post': 'create', 'get': 'list'})),
    path('game_news/<int:pk>', NewsViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
]

router.register(r"admins", admin.AdminViewSet, base_name="admin")

report_urls = [
    path('report', report.ReportViewSet.as_view({'get': 'list'}), name='report-list'),
    path('report/<int:pk>', report.ReportViewSet.as_view({'get': 'retrieve'}), name='report-detail'),
    path('report/<int:pk>/proved_false', report.proved_false),
    path('report/<int:pk>/do_delete', report.do_delete),
]

banner_urls = [
    path('banners', BannerViewSet.as_view({'get': 'list', 'post': 'create'}), name='banner-list'),
    path('banners/<int:pk>', BannerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='banner-detail'),
]

financial_management_urls = [
    path("withdraw_logs", WithdrawLogViewSet.as_view({"get": "list"})),
    re_path("^withdraw_logs/(?P<pk>\d+)/(?P<operate>(approved|rejected))$",
            WithdrawLogViewSet.as_view({"put": "update"})),
    path("pay_orders", PayOrdersViewSet.as_view({"get": "list"}))
]

user_management_urls = [
    path('coin/change', CoinChangLogViewSet.as_view({'post': 'create'}), name='coin_change'),
    path('coin/change/log', CoinChangLogViewSet.as_view({"get": "list"}), name='coin_change_log'),
    path("users", UserManagementViewSet.as_view({"get": "list"})),
    path("money_change_logs/<int:pk>", MoneyBalanceChangeLogViewSet.as_view({"get": "list"})),
    path("edit_user/<int:pk>", EditUserInfo.as_view({"put": "update"}))
]

official_account_change_logs_urls = [
    path("official_account_change_logs", OfficialAccountChangeLogsViewSet.as_view({"get": "list"}))
]

message_urls = [
    path('messages', MessageViewSet.as_view({'get': 'list'}), name='message'),
    path('messages/<int:pk>', MessageViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'}), name='message'),
]

album_url = [
    path('albums', AlbumViewSet.as_view({"get": "list", "post": "create"}), name='album_list'),
    path('albums/<int:pk>', AlbumViewSet.as_view({"get": "retrieve", "patch": "partial_update"}), name='album_modify'),
    path('albums/<int:album_id>/pictures', AlbumPictureViewSet.as_view({"get": "list", "post": "create"}), name='picture_list'),
]

router.register(r"word_filters", WordFilterViewSet)

urlpatterns = router.urls
urlpatterns += boxer_url
urlpatterns += course_url
urlpatterns += club_url
urlpatterns += login_urls
urlpatterns += hot_video_url
urlpatterns += upload_url
urlpatterns += captcha_urls
urlpatterns += news_urls
urlpatterns += report_urls
urlpatterns += banner_urls
urlpatterns += financial_management_urls
urlpatterns += user_management_urls
urlpatterns += official_account_change_logs_urls
urlpatterns += message_urls
urlpatterns += album_url

if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
