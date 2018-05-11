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
from django.urls import path

from boxing_console.views.boxer_approve import BoxerIdentificationViewSet
from boxing_console.views.club import BoxingClubVewSet
from boxing_console.views.coin_and_money import CoinChangLogViewSet, MoneyChangeLogViewSet
from boxing_console.views.course import CourseViewSet
from boxing_console.views.user_management import UserManagementViewSet

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

course_url = [
    path('courses', CourseViewSet.as_view({'get': 'list'}), name='courses_list'),
    path('course/<int:pk>', CourseViewSet.as_view({'get': 'retrieve'}), name='course_detail')
]

club_url = [
    path('club', BoxingClubVewSet.as_view({'post': 'create'})),
    path('club/<int:pk>',BoxingClubVewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]

urlpatterns += boxer_url
urlpatterns += course_url
urlpatterns += club_url
