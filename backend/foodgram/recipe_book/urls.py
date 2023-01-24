from django.urls import include, path
from recipe_book.views import (FavoriteViewSet, IngredientsViewSet,
                               RecipesViewSet, ShoppingCartViewSet,
                               SubscriptionsViewSet, TagsViewSet)
from rest_framework.routers import DefaultRouter

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet)
v1_router.register('tags', TagsViewSet)
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register('users/subscriptions', SubscriptionsViewSet,
                   basename='subscriptions')

urlpatterns = [
    path(r'recipes/download_shopping_cart/',
         ShoppingCartViewSet.as_view(
             {'get': 'download_shopping_cart'}), ),
    path(r'recipes/<int:pk>/favorite/',
         FavoriteViewSet.as_view(
             {'post': 'favorite', 'delete': 'favorite'}), ),
    path(r'recipes/<int:pk>/shopping_cart/',
         ShoppingCartViewSet.as_view(
             {'post': 'shopping_cart', 'delete': 'shopping_cart'}), ),
    path(r'users/<int:pk>/subscribe/',
         SubscriptionsViewSet.as_view(
             {'post': 'subscribe', 'delete': 'subscribe'}), ),
    path('', include(v1_router.urls)),
]
