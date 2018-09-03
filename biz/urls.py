from django.urls import path
from biz.views import AuthTokenLogin
from biz.views import logout

login_urls = [
    path("login", AuthTokenLogin.as_view()),
    path("logout", logout)
]


urlpatterns = []
urlpatterns += login_urls