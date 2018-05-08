"""boxing_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from boxing_app.views import upload
from boxing_app.views.boxer import BoxerIdentificationViewSet
from boxing_app.views import message
from boxing_app.views import comment
from boxing_app.views import report
from boxing_app.views import like
from boxing_app.views import follow
from biz.constants import REPORT_OBJECT_DICT, COMMENT_OBJECT_DICT

boxer_identification = BoxerIdentificationViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'retrieve'})

discover_urls = [
    path('messages', message.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-latest'),
    path('messages/hot', message.MessageViewSet.as_view({'get': 'hot'}), name='message-hot'),
    path('messages/<int:pk>', message.MessageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='message-detail'),
    path('messages/<int:message_id>/like', like.LikeViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='messgae-like'),
]

comment_object_string = '|'.join(COMMENT_OBJECT_DICT.keys())
comment_urls = [
    re_path(r'^(?P<object_type>({0}))s/(?P<object_id>\d+)/comments$'.format(comment_object_string), comment.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    re_path(r'^(?P<object_type>({0}))s/(?P<object_id>\d+)/comments/(?P<pk>\d+)$'.format(comment_object_string), comment.ReplyViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='comment-detail'),
]

upload_urls = [
    path('upload_file', upload.upload_file, name='upload'),
]

report_object_string = '|'.join(REPORT_OBJECT_DICT.keys())
report_urls = [
    re_path(r'^(?P<object_type>({0}))s/report$'.format(report_object_string), report.ReportViewSet.as_view({'post': 'create'}), name='report'),
    path('report_reason', report.ReportViewSet.as_view({'get': 'retrieve'}), name='report-reason')
]

boxer_url = [
    path('boxer/identification', boxer_identification, name='boxer_identification'),
]

follow_url = [
    path('follow', follow.BaseFollowView.as_view()),
    path('follower', follow.FollowerView.as_view()),
    path('followed', follow.FollowedView.as_view()),
    path('unfollow', follow.UnFollowView.as_view()),
]

urlpatterns = []
urlpatterns += upload_urls
urlpatterns += boxer_url
urlpatterns += discover_urls
urlpatterns += comment_urls
urlpatterns += report_urls
urlpatterns += follow_url
if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
    urlpatterns += static(settings.BASE_UPLOAD_FILE_URL, document_root=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR)
