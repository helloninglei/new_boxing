"""boxing_console URL Configuration

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
from django.contrib import admin

from boxing_console.views.coin_and_money import CoinChangLogViewSet, add_or_subtract_user_coin, \
    add_or_subtract_user_money
from boxing_console.views.user_management import UserManagementViewSet


urlpatterns = [

    # url(r'^admin/', admin.site.urls),
    url(r"^users$", UserManagementViewSet.as_view({"get": "list"})),
    url(r'^admin/', admin.site.urls),
    url(r'^add-subtract-coin/(?P<effect_user_id>\d+)', add_or_subtract_user_coin,
        name='add_or_subtract_coin'),
    url(r'^add-subtract-money/(?P<effect_user_id>\d+)', add_or_subtract_user_money,
        name='add_or_subtract_money'),
    url(r'^coin-change-log$',CoinChangLogViewSet.as_view({"get": "list"}), name='coin_change_log_list'),
]
