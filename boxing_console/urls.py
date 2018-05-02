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
from django.urls import path

from boxing_console.views.coin_and_money import CoinChangLogViewSet, MoneyChangeLogViewSet
from boxing_console.views.user_management import UserManagementViewSet


urlpatterns = [
    path('coin/change', CoinChangLogViewSet.as_view({'post':'create'}),
        name='coin_change'),
    url('money/change', MoneyChangeLogViewSet.as_view({'post':'create'}),
        name='money_change'),
    url('coin/change/log',CoinChangLogViewSet.as_view({"get": "list"}), name='coin_change_log'),
    url("users", UserManagementViewSet.as_view({"get": "list"}))
]
