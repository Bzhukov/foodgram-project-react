from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import (RecipesViewSet, TagsViewSet, IngredientsViewSet,
                               SubscriptionsViewSet, FavoriteViewSet,
                               ShoppingCartViewSet)

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet)
v1_router.register('tags', TagsViewSet)
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register(r'recipes', FavoriteViewSet,
                   basename='favorite')
v1_router.register('users/subscriptions', SubscriptionsViewSet,
                   basename='subscriptions')
v1_router.register(r'users',
                   SubscriptionsViewSet,
                   basename='subscribe'),
v1_router.register('recipes',
                   ShoppingCartViewSet,
                   basename='shopping_cart')

urlpatterns = [
    path('', include(v1_router.urls)),
]
