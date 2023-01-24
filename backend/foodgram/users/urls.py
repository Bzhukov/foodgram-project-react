from django.urls import include, path
from users.views import CustomAuthToken

app_name = 'users'

urlpatterns = [
    path('auth/token/login/', CustomAuthToken.as_view(), name='get_token'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
