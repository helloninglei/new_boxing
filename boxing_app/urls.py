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
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from boxing_app.views import upload
from boxing_app.views.boxer import BoxerIdentificationViewSet
from boxing_app.views import message
from boxing_app.views import comment
from boxing_app.views import report
from boxing_app.views import like

boxer_identification = BoxerIdentificationViewSet.as_view({'post': 'create', 'put': 'update', 'get': 'retrieve'})

discover_urls = [
    path('messages', message.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-latest'),
    path('messages/hot', message.MessageViewSet.as_view({'get': 'hot'}), name='message-hot'),
    path('messages/<int:pk>', message.MessageViewSet.as_view({'get': 'retrieve', 'delete': 'destroy'}), name='message-detail'),
    path('messages/<int:message_id>/comments', comment.CommentViewSet.as_view({'get': 'list', 'post': 'create'}), name='comment-list'),
    path('messages/<int:message_id>/comments/<int:pk>', comment.ReplyViewSet.as_view({'post': 'create', 'delete': 'destroy'}), name='comment-detail'),
    path('messages/<int:message_id>/like', like.LikeViewSet.as_view({'get': 'list', 'post': 'create', 'delete': 'destroy'}), name='messgae-like'),
    path('messages/<int:message_id>/report', report.ReportViewSet.as_view({'post': 'create'}), name='message-report'),
]

upload_urls = [
    path('upload_file', upload.upload_file, name='upload'),
]

boxer_url = [
    path('boxer/identification', boxer_identification, name='boxer_identification'),
]

urlpatterns = []
urlpatterns += upload_urls
urlpatterns += boxer_url
urlpatterns += discover_urls
if settings.ENVIRONMENT != settings.PRODUCTION:
    urlpatterns += [path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))]
    urlpatterns += static(settings.BASE_UPLOAD_FILE_URL, document_root=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR)
