from django.urls import include, path
from rest_framework.routers import DefaultRouter

#from .views import get_user_token_auth, send_user_code

router_ver1 = DefaultRouter()

urlpatterns = [
    path('v1/', include(router_ver1.urls)),
    #path('v1/auth/signup/', send_user_code, name='signup'),
    #path('v1/auth/token/', get_user_token_auth, name='token')
]
