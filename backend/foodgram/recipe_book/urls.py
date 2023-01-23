from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import (SubscriptionsViewSet,
                               ShoppingCartViewSet,
                               FavoriteViewSet,
                               IngredientsViewSet,
                               TagsViewSet,
                               RecipesViewSet)

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet)
v1_router.register('tags', TagsViewSet)
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register('recipes', FavoriteViewSet,
                   basename='favorite')
v1_router.register('users/subscriptions', SubscriptionsViewSet,
                   basename='subscriptions')
v1_router.register('recipes',
                   ShoppingCartViewSet,
                   basename='shopping_cart')

urlpatterns = [
    path(r'users/<int:pk>/subscribe/',
         SubscriptionsViewSet.as_view(
             {'post': 'subscribe', 'delete': 'subscribe'}), ),
    path('', include(v1_router.urls)),
]
