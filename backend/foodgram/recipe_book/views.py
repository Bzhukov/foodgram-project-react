from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipe_book.models import Recipe, Tag, Ingredient
from recipe_book.permission import IsAdminOrReadOnly
from recipe_book.serializers import (RecipeSerializer, TagSerializer,
                                     IngredientSerializers)


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех рецептов.
    Права доступа: Администратор или только чтение.
    """
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = RecipeSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('author', 'name',)

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Получение списка всех Тегов.
    Права доступа: Всем.
    """
    queryset = Tag.objects.all()
    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination
    serializer_class = TagSerializer
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
    pagination_class = PageNumberPagination
    serializer_class = IngredientSerializers
    search_fields = ('name',)

    def retrieve(self, request, pk=None):
        queryset = Ingredient.objects.all()
        ingredient= get_object_or_404(queryset, pk=pk)
        serializer = IngredientSerializers(ingredient)
        return Response(serializer.data)
