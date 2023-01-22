from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import (RecipesViewSet, TagsViewSet, IngredientsViewSet,
                               SubscriptionsViewSet, FavoriteViewSet,
                               ShoppingCartViewSet)

v1_router = DefaultRouter()
v1_router.register('recipes/download_shopping_cart', ShoppingCartViewSet,
                   basename='shopping_cart')
v1_router.register('recipes', RecipesViewSet)
v1_router.register(r'recipes/(?P<recipe_id>[\d]+)/favorite', FavoriteViewSet,
                   basename='Favorite')
v1_router.register('tags', TagsViewSet)
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register('users/subscriptions', SubscriptionsViewSet,
                   basename='subscriptions')
v1_router.register(r'users/(?P<author_id>[\d]+)/subscribe',
                   SubscriptionsViewSet,
                   basename='subscribe'),
v1_router.register('recipes/(?P<recipe_id>[\d]+)/shopping_cart',
                   ShoppingCartViewSet,
                   basename='shopping_cart')

urlpatterns = [
    path('', include(v1_router.urls)),
]
