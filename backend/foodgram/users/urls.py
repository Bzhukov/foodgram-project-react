from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomAuthToken, CustomUserViewSet

app_name = 'users'
router = DefaultRouter()

router.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/token/login/', CustomAuthToken.as_view(), name='get_token'),
    path('auth/', include('djoser.urls.authtoken')),
]
