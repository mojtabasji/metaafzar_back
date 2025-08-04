from django.urls import path, include
from rest_framework import permissions
from my_scraper import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from my_scraper import components

schema_view = get_schema_view(
    openapi.Info(
        title="MetaAfzar API",
        default_version='v1',
        description="API documentation for MetaAfzar project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="mojtaba@bytecraft.ir"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes= [permissions.AllowAny,]
)

urlpatterns = [
    path('list/', components.endpoints_list, name='endpoints-list'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('users', views.UserListView.as_view()),
    path('users/register', views.UserRegisterView.as_view()),
    path('users/<int:id>', views.UserDetailView.as_view()),
    path('users/login', views.UserLoginView.as_view()),
    path('users/auth_check', views.UserAuthCheckView.as_view()),
    path('users/logout', views.UserLogoutView.as_view()),
    path('users/igpages', views.UserIGPageListView.as_view()),
    path('users/attach_igpage', views.AttachNewIGPageView.as_view()),
    path('igpages', views.IGPageListView.as_view()),
    path('igpages/<int:id>', views.IGPageDetailView.as_view()),
]