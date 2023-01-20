from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import permissions
from rest_framework import viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from recipe_book.filters import IngredientFilter, RecipeFilter
from recipe_book.models import (Recipe, Tag, Ingredient, Subscription,
                                Favorite, Shopping_cart)
from recipe_book.permission import IsAuthorOrReadOnly, IsAdminOrReadOnly
from recipe_book.serializers import (RecipeReadSerializer, TagSerializer,
                                     IngredientSerializers,
                                     SubscriptionSerializers,
                                     ShoppingCartSerializer,
                                     RecipeWriteSerializer, FavoriteSerializer
                                     )

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов.
    Права доступа: Администратор или только чтение.
    """
    queryset = Recipe.objects.all()
    # pagination_class = PageNumberPagination
    http_method_names = ['post', 'get', 'delete', 'patch']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.action in ['retrieve', ]:
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['perform_create', 'perform_update']:
            permission_classes = [IsAuthorOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def retrieve(self, request, pk=None,*args, **kwargs):
        recipe = get_object_or_404(Recipe, pk=pk)
        serializer = RecipeReadSerializer(recipe, context={'request': request})
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет Тегов.
    Права доступа: Всем.
    """
    queryset = Tag.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    serializer_class = TagSerializer
    http_method_names = ['get', ]
    search_fields = ('name', 'slug')

    def retrieve(self, request, pk=None,*args, **kwargs):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет Ингридиентов.
    Права доступа: Читать всем, изменять только суперадмину.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = IngredientSerializers
    http_method_names = ['post', 'get', 'delete', 'patch']
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('name',)

    def retrieve(self, request, pk=None,*args, **kwargs):
        queryset = Ingredient.objects.all()
        ingredient = get_object_or_404(queryset, pk=pk)
        serializer = IngredientSerializers(ingredient)
        return Response(serializer.data)


class SubscriptionsViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Подписок
    Права доступа: Всем авторизованным.
    """
    serializer_class = SubscriptionSerializers
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get', 'delete']

    def get_queryset(self):
        return Subscription.objects.select_related().filter(
            user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset=Subscription.objects.select_related().filter(
            user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        author_id = self.kwargs.get('author_id')
        user_id = self.request.user.id
        queryset = Subscription.objects.filter(
            author_id=author_id,
            user_id=user_id)
        if queryset.exists():
            raise ValidationError('Вы уже подписаны на данного автора')
        if author_id == user_id:
            raise ValidationError('Нельзя подписаться на себя')
        serializer.save(user_id=user_id, author_id=author_id)

    def delete(self, request, author_id):
        try:
            instance = get_object_or_404(Subscription,
                                         user_id=request.user.id,
                                         author_id=author_id)
            self.perform_destroy(instance)
        except Http404:
            raise ValidationError('Вы не подписаны на данного автора')
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Избранного
    Права доступа: Всем авторизованным.
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer
    http_method_names = ['post', 'get', 'delete']

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        user_id = self.request.user.id
        queryset = Favorite.objects.filter(
            recipe_id=recipe_id,
            user_id=user_id)
        if queryset.exists():
            raise ValidationError('Данный рецепт уже добавлен в избранное')
        serializer.save(user_id=user_id, recipe_id=recipe_id)

    def delete(self, request, recipe_id):
        try:
            instance = get_object_or_404(Favorite,
                                         user_id=request.user.id,
                                         recipe_id=recipe_id)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Корзины
    Права доступа: автору.
    """
    serializer_class = ShoppingCartSerializer
    http_method_names = ['post', 'get', 'delete']
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = Shopping_cart.objects.all()

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('recipe_id')
        user_id = self.request.user.id
        queryset = Shopping_cart.objects.filter(
            recipe_id=recipe_id,
            user_id=user_id)
        if queryset.exists():
            raise ValidationError('Данный рецепт уже добавлен в корзину')
        serializer.save(user_id=user_id, recipe_id=recipe_id)

    def delete(self, request, recipe_id):
        try:
            instance = get_object_or_404(Shopping_cart,
                                         user_id=request.user.id,
                                         recipe_id=recipe_id)
            self.perform_destroy(instance)
        except Http404:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        ingredients = Ingredient.objects.filter(
            recipe__shopping_carts__user=request.user).values(
            'name',
            'measurement_unit'
        ).annotate(amount=Sum('structure__amount'))
        today = datetime.today()
        shopping_list = (
            f'Список покупок для: {request.user.get_full_name()}\n\n'
            f'Дата: {today:%Y-%m-%d}\n\n'
        )
        shopping_list += '\n'.join([
            f'- {ingredient["name"]} '
            f'({ingredient["measurement_unit"]})'
            f' - {ingredient["amount"]}'
            for ingredient in ingredients
        ])
        filename = f'{request.user.username}_shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
