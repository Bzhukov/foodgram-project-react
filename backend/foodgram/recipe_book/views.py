from datetime import datetime

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from recipe_book.filters import IngredientFilter, RecipeFilter
from recipe_book.models import (Favorite, Ingredient, Recipe, ShoppingCart,
                                Subscription, Tag)
from recipe_book.pagination import LimitPageNumberPagination
from recipe_book.permission import IsAdminOrReadOnly, IsAuthorOrReadOnly
from recipe_book.serializers import (FavoriteSerializer, IngredientSerializers,
                                     RecipeReadSerializer,
                                     RecipeWriteSerializer,
                                     ShoppingCartReadSerializer,
                                     ShoppingCartWriteSerializer,
                                     SubscriptionReadSerializer,
                                     SubscriptionWriteSerializer,
                                     TagSerializer)
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

User = get_user_model()


class RecipesViewSet(viewsets.ModelViewSet):
    """
    Вьюсет рецептов.
    Права доступа: Администратор или только чтение.
    """
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    http_method_names = ('post', 'get', 'delete', 'patch')
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
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


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет Ингридиентов.
    Права доступа: Читать всем, изменять только суперадмину.
    """
    queryset = Ingredient.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = IngredientSerializers
    http_method_names = ['get', ]
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter
    search_fields = ('name',)


class SubscriptionsViewSet(mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin,
                           GenericViewSet):
    """
    Вьюсет Подписок
    Права доступа: Всем авторизованным.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionReadSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['post', 'get', 'delete']
    pagination_class = LimitPageNumberPagination

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk=None):
        if request.method == 'DELETE':
            instance = get_object_or_404(Subscription,
                                         user_id=request.user.id,
                                         author_id=pk)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            serializer = SubscriptionWriteSerializer(
                data={'user': request.user.pk, 'author': pk},
                context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      GenericViewSet):
    """
    Вьюсет Избранного
    Права доступа: Всем авторизованным.
    """
    queryset = Favorite.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FavoriteSerializer
    http_method_names = ['post', 'delete']

    def get_queryset(self):
        return Subscription.objects.select_related().filter(
            user=self.request.user)

    @action(detail=True, methods=['post', 'delete'], )
    def favorite(self, request, pk=None):
        if request.method == 'DELETE':
            instance = get_object_or_404(Favorite,
                                         user_id=request.user.id,
                                         recipe_id=pk)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            serializer = self.serializer_class(
                data={'user': request.user.pk, 'recipe': pk},
                context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    Вьюсет Корзины
    Права доступа: автору.
    """
    serializer_class = ShoppingCartReadSerializer
    http_method_names = ['post', 'get', 'delete']
    permission_classes = (IsAuthorOrReadOnly,)
    queryset = ShoppingCart.objects.all()

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk=None):
        if request.method == 'DELETE':
            instance = get_object_or_404(ShoppingCart,
                                         user_id=request.user.id,
                                         recipe_id=pk)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if request.method == 'POST':
            serializer = ShoppingCartWriteSerializer(
                data={'user': request.user.id, 'recipe': pk},
                context={'request': self.request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(
            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
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
