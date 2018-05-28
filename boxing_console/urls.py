"""boxing_console URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.urls import include, path, re_path
from django.conf import settings
from boxing_console.views.boxer_approve import BoxerIdentificationViewSet
from boxing_console.views.club import BoxingClubVewSet
from boxing_console.views.coin_and_money import CoinChangLogViewSet, MoneyChangeLogViewSet
from boxing_console.views.course import CourseViewSet, CourseOrderViewSet
from boxing_console.views.user_management import UserManagementViewSet
from boxing_console.views.hot_video import HotVideoViewSet
from boxing_console.views.game_news import NewsViewSet
from boxing_console.views.banner import BannerViewSet
from boxing_console.views.report import ReportViewSet, ReportHandleViewSet
from biz.views import upload_file, captcha_image
from boxing_console.views import admin
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('coin/change', CoinChangLogViewSet.as_view({'post': 'create'}), name='coin_change'),
    path('money/change', MoneyChangeLogViewSet.as_view({'post': 'create'}), name='money_change'),
    path('coin/change/log', CoinChangLogViewSet.as_view({"get": "list"}), name='coin_change_log'),
    path("users", UserManagementViewSet.as_view({"get": "list"}))
]

boxer_url = [
    path('boxer/identification', BoxerIdentificationViewSet.as_view({'get': 'list'}), name='boxer_identification_list'),
    path('boxer/identification/<int:pk>', BoxerIdentificationViewSet.as_view({'get': 'retrieve'}),
         name='boxer_identification_detail'),
    path('boxer/identification/<int:pk>/<lock_type>(LOCK|UNLOCK)',
         BoxerIdentificationViewSet.as_view({'post': 'change_lock_state'}), name='change_lock_state'),
    path('boxer/identification/<int:pk>/approve', BoxerIdentificationViewSet.as_view({'post': 'approve'}),
         name='identification_approve'),
    path('boxer/identification/<int:pk>/refuse', BoxerIdentificationViewSet.as_view({'post': 'refuse'}),
         name='identification_refuse'),
]

hot_video_url = [
    path('hot_videos', HotVideoViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('hot_videos/<int:pk>',
         HotVideoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy', 'patch': 'partial_update'})),
]

course_url = [
    path('courses', CourseViewSet.as_view({'get': 'list'}), name='courses_list'),
    path('course/<int:pk>', CourseViewSet.as_view({'get': 'retrieve'}), name='course_detail'),
    path('course/orders', CourseOrderViewSet.as_view({'get': 'list'})),
    path('course/order/<int:pk>', CourseOrderViewSet.as_view({'get': 'retrieve'})),
]

club_url = [
    path('club', BoxingClubVewSet.as_view({'post': 'create', 'get': 'list'})),
    path('club/<int:pk>', BoxingClubVewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
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
    path('report', ReportViewSet.as_view({'get': 'list'}), name='report-list'),
    path('report/<int:pk>', ReportViewSet.as_view({'get': 'retrieve'}), name='report-detail'),
    path('report/<int:pk>/proved_false', ReportHandleViewSet.as_view({'post': 'proved_false'})),
    path('report/<int:pk>/do_delete', ReportHandleViewSet.as_view({'post': 'do_delete'})),
]

banner_urls = [
    path('banners', BannerViewSet.as_view({'get': 'list', 'post': 'create'}), name='banner-list'),
    path('banners/<int:pk>', BannerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name='banner-detail'),
]

urlpatterns += router.urls
urlpatterns += boxer_url
urlpatterns += course_url
urlpatterns += club_url
urlpatterns += login_urls
urlpatterns += course_url
urlpatterns += hot_video_url
urlpatterns += upload_url
urlpatterns += captcha_urls
urlpatterns += news_urls
urlpatterns += report_urls
urlpatterns += banner_urls

if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
