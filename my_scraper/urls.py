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
    # path('user/igpages/', views.UserIGPageListView.as_view(), name='user-igpages'),
    # path('igpages/', views.IGPageListView.as_view(), name='igpage-list'),
    # path('igpages/attach/', views.AttachNewIGPageView.as_view(), name='attach-igpage'),
    # path('igpages/<int:pk>/', views.IGPageDetailView.as_view(), name='igpage-detail'),
    # path('igpages/<int:pk>/scrape/', views.ScrapeIGPageView.as_view(), name='scrape-igpage'),
    path('users/ig/getconnectlink', views.get_connect_link, name='get-connect-link'),
    path('testing/', views.testing, name='testing'),
]