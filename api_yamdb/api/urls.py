from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_ver1 = DefaultRouter()

router_ver1.register(r'users', views.UserViewSet)

urlpatterns = [
    path('v1/auth/signup/', views.signup_user, name='signup'),
    path('v1/auth/token/', views.get_auth_token, name='auth'),
    path('v1/', include(router_ver1.urls)),
]
