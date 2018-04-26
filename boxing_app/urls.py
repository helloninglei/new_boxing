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
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from boxing_app.views import upload
from boxing_app.views.boxer import BoxerIdentificationViewSet
from boxing_app.views import message


message_urls = [
    url(r"^messages$", message.MessageViewSet.as_view({'get': 'list', 'post': 'create'}), name='message-latest'),
    url(r"^messages/hot$", message.MessageViewSet.as_view({'get': 'hot'}), name='message-hot'),
    url(r'^messages/(?P<pk>[0-9]+)$', message.MessageViewSet.as_view({'get': 'retrieve','delete': 'destroy'}), name='message-detail'),
]

upload_urls = [
    url(r'^upload_file$', upload.upload_file, name='upload'),
]
boxer_url = [
    url(r'^boxer/identification/create$',BoxerIdentificationViewSet.as_view({'post':'create'}), name='identification_create'),
]

urlpatterns = upload_urls + boxer_url + upload_urls + message_urls
urlpatterns += static(settings.BASE_UPLOAD_FILE_URL, document_root=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR)
urlpatterns += static(settings.BASE_UPLOAD_FILE_URL, document_root=settings.UPLOAD_FILE_LOCAL_STORAGE_DIR)
