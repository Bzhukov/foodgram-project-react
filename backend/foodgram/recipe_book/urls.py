from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import RecipesViewSet

v1_router = DefaultRouter()
v1_router.register(r'recipes', RecipesViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
