from django.urls import include, path

from users.views import CustomAuthToken

urlpatterns = [

    path('', include('djoser.urls')),
    path('auth/token/login/', CustomAuthToken.as_view(), name='get_token'),
    path('auth/', include('djoser.urls.authtoken')),
]
