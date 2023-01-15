from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import filters, viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination)
from rest_framework.response import Response

from recipe_book.filters import IngredientFilter, RecipeFilter
from recipe_book.models import Recipe, Tag, Ingredient, Subscription
from recipe_book.permission import IsAuthorOrReadOnly
from recipe_book.serializers import (RecipeSerializer, TagSerializer,
                                     IngredientSerializers,
                                     SubscriptionSerializers,
                                     SubscriptionSerializers2, )

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
    pagination_class = PageNumberPagination

    def get_queryset(self):
        subscriptions = Subscription.objects.select_related().filter(
            user=self.request.user)
        return subscriptions.all()

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request):
        return Response(status=status.HTTP_204_NO_CONTENT)
        # print('111', user_id)
        # user = self.request.user
        # author = get_object_or_404(User, pk=user_id)
        # is_subscribed = get_object_or_404(Subscription, user=user,
        #                                   author=author)
        # data = {'user': user, 'author': author}
        # serializer = SubscriptionSerializers(
        #     data=data,
        #     context={'request': request},
        #     partial=True
        # )
        # serializer.is_valid(raise_exception=True)
        # if request.method == 'POST':
        #     print('222', user_id)
        #     Subscription.objects.create(user=user, author=author)
        #     serializer = SubscriptionSerializers(
        #         author,
        #         context={'request': request}
        #     )
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if request.method == 'DELETE':
        #     is_subscribed.delete()
        #     return Response(status=status.HTTP_204_NO_CONTENT)

    # @action(
    #     detail=True,
    #     methods=['GET'],
    #     permission_classes=(permissions.IsAuthenticated,)
    # )
    # def subscriptions(self, request):
    #     print('111')
    #     user = self.request.user
    #     serializer = SubscriptionSerializers(
    #         user,
    #         context={'request': request}
    #     )
    #     return self.get_paginated_response(serializer.data)
    #

    @action(
        detail=True,
        methods=['GET'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        print('333')
        subscriptions = Subscription.objects.select_related().filter(
            user=self.request.user)
        serializer = SubscriptionSerializers(subscriptions,
                                             context={'request': request},
                                             many=True)
        return Response(serializer.data)

class SubscriptionsViewSet2(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializers2

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=(permissions.IsAuthenticated,),
    )
    def subscribe(self, request, pk):
        print(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)