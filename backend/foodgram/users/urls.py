from django.urls import path, include

from users.views import get_jwt_token

auth_path = [
    path('token/login/', get_jwt_token, name='get_token'),
]

urlpatterns = [
    path('auth/', include(auth_path)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
