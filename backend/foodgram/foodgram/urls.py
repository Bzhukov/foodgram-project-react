from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('api/', include('recipe_book.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),

]
