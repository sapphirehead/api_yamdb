from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
from reviews.views import ReviewViewSet, CommentViewSet

router_ver1 = DefaultRouter()

router_ver1.register(r'users', views.UserViewSet)
router_ver1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
)
router_ver1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments',
    CommentViewSet
)

urlpatterns = [
    path('v1/auth/signup/', views.signup_user, name='signup'),
    path('v1/auth/token/', views.get_auth_token, name='auth'),
    path('v1/', include(router_ver1.urls)),
]
