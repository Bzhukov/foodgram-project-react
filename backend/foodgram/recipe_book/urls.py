from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import (RecipesViewSet, TagsViewSet, IngredientsViewSet,
                               SubscriptionsViewSet)

v1_router = DefaultRouter()
v1_router.register(r'recipes', RecipesViewSet)
v1_router.register(r'tags', TagsViewSet)
v1_router.register(r'ingredients', IngredientsViewSet)
v1_router.register(r'subscriptions', SubscriptionsViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
]
