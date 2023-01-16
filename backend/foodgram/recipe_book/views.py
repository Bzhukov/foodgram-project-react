from django.contrib.auth import get_user_model
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import (LimitOffsetPagination)
from rest_framework.response import Response

from recipe_book.filters import IngredientFilter, RecipeFilter
from recipe_book.models import Recipe, Tag, Ingredient, Subscription
from recipe_book.permission import IsAuthorOrReadOnly
from recipe_book.serializers import (RecipeSerializer, TagSerializer,
                                     IngredientSerializers,
                                     SubscriptionSerializers,
                                     )

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех рецептов.
    Права доступа: Администратор или только чтение.
    """
    queryset = Recipe.objects.all()
    # pagination_class = PageNumberPagination
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (filters.SearchFilter,)
    # filter_backends = (DjangoFilterBackend,)
    search_fields = ('author', 'name',)

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка всех Тегов.
    Права доступа: Всем.
    """
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = LimitOffsetPagination
    serializer_class = TagSerializer
    filterset_class = RecipeFilter
    search_fields = ('name',)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка всех Ингридиентов.
    Права доступа: Всем.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = IngredientSerializers
    pagination_class = None
    filterset_class = IngredientFilter
    search_fields = ('name',)

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        ingredient = get_object_or_404(queryset, pk=pk)
        serializer = IngredientSerializers(ingredient)
        return Response(serializer.data)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializers

    def get_queryset(self):
        return Subscription.objects.select_related().filter(
            user=self.request.user)

    def list(self, request):
        serializer = SubscriptionSerializers(self.queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        author_id = self.kwargs.get('author_id')
        user_id = self.request.user.id
        queryset = Subscription.objects.filter(
            author_id=author_id,
            user_id=user_id)
        if queryset.exists():
            raise ValidationError('Вы уже подписаны на данного автора')
        serializer.save(user_id=user_id, author_id=author_id)

    def delete(self, request, author_id):
        try:
            instance = get_object_or_404(Subscription,
                                         user_id=request.user.id,
                                         author_id=author_id)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
