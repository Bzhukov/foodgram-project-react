from django.urls import include, path

from users.views import get_jwt_token

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/', get_jwt_token, name='get_token'),
    path('auth/', include('djoser.urls.authtoken')),
]
