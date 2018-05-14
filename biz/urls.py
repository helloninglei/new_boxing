from django.urls import path
from biz.views import AuthTokenLogin

login_urls = [
    path("login", AuthTokenLogin.as_view())
]


urlpatterns = []
urlpatterns += login_urls
