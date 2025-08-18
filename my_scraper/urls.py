from django.urls import path, include
from rest_framework import permissions
from my_scraper import views
from my_scraper import components
from django.conf import settings

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('', views.UserViewSetApiView, basename='user')

urlpatterns = [
    path('users/', include(router.urls)),
    path('users/ig/getconnectlink', views.get_connect_link, name='get-connect-link'),
    path('testing/', views.testing, name='testing'),
]