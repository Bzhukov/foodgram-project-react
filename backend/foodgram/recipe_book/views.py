from rest_framework import filters, permissions, serializers, status, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from recipe_book.models import Recipe
from recipe_book.permission import IsAdminOrReadOnly
from recipe_book.serializers import RecipeSerializer


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
    search_fields = ('author', )

    def retrieve(self, request, pk=None):
        queryset = Recipe.objects.all()
        recipe = get_object_or_404(queryset, pk=pk)

        serializer = RecipeSerializer(recipe)
        return Response(serializer.data)
