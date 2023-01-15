from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe_book.views import (RecipesViewSet, TagsViewSet, IngredientsViewSet,
                               SubscriptionsViewSet)

v1_router = DefaultRouter()
v1_router.register('recipes', RecipesViewSet)
v1_router.register('tags', TagsViewSet)
v1_router.register('ingredients', IngredientsViewSet)
v1_router.register('users/subscriptions', SubscriptionsViewSet,
                   basename='subscriptions')
v1_router.register(r'users/(?P<user_id>[\d]+)/subscribe', SubscriptionsViewSet,
                   basename='subscribe')


urlpatterns = [
    path('', include(v1_router.urls)),
]
