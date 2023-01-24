import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from recipe_book.models import (Favorite, Ingredient, Recipe, ShoppingCart,
                                Structure, Subscription, Tag)
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from foodgram.settings import MAX_INGREDIENT_AMOUNT, MIN_INGREDIENT_AMOUNT

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор Тэгов."""

    class Meta:
        model = Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор авторов."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Subscription.objects.filter(author=obj, user=user).exists()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit',)

    def get_amount(self, obj):
        return obj.structure.first().amount


class StructureSerializer(serializers.ModelSerializer):
    """Сериализатор состава рецепта."""
    id = serializers.IntegerField()
    amount = serializers.IntegerField(
        validators=[MaxValueValidator(MAX_INGREDIENT_AMOUNT),
                    MinValueValidator(MIN_INGREDIENT_AMOUNT)])

    class Meta:
        model = Structure
        fields = ('id', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для чтения данных"""
    tags = TagSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True, many=False)
    ingredients = IngredientSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True, allow_null=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'ingredients', 'tags',)
        lookup_field = 'name'

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        user = request.user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(recipe=obj, user=user).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов для записи данных"""
    author = AuthorSerializer(read_only=True, many=False)
    ingredients = StructureSerializer(read_only=False, many=True)
    image = Base64ImageField(required=True, allow_null=False)

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients', 'name', 'image', 'text',
                  'cooking_time')

    def create_ingredients(self, ingredients, recipe):
        Structure.objects.bulk_create([Structure(
            ingredients=get_object_or_404(Ingredient, pk=ingredient.get('id')),
            recipe=recipe,
            amount=int(ingredient.get('amount'))
        ) for ingredient in ingredients])

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Мин. 1 ингредиент в рецепте!')

        if len(ingredients) > len(set(
                dict(ingredient.items())['id'] for ingredient in
                ingredients)):
            # OrderDict напрямую в set не переводится, поэтому пришлось
            # использовать такую ивзращенную конструкцию. Понимаю что это
            # плохо, но цикла избежать не удалось
            raise serializers.ValidationError({
                'ingredients': 'Ингредиенты дублируется в данном рецепте!'})
        return ingredients

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        user = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.name = validated_data.get('name', instance.name)
        instance.image = validated_data.get('content', instance.image)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get('cooking_time',
                                                   instance.cooking_time)
        instance.author_id = user.id
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context=self.context).data


class IngredientSerializers(serializers.ModelSerializer):
    """Сериализатор ингредиентов"""
    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('__all__')

    def get_measurement_unit(self, obj):
        return obj.get_measurement_unit_display()


class SubscriptionReadSerializer(serializers.ModelSerializer):
    """Сериализатор подписок для чтения данных"""
    email = serializers.EmailField(source='author.email',
                                   read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='author',
                                            read_only=True)
    username = serializers.CharField(source='author.username',
                                     read_only=True)
    first_name = serializers.CharField(source='author.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='author.last_name',
                                      read_only=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'recipes',
            'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipe.objects.filter(author=obj.author)
        if limit:
            recipes = recipes[:int(limit)]
        context = {'request': request}
        return RecipeReadSerializer(recipes, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()


class SubscriptionWriteSerializer(serializers.ModelSerializer):
    """Сериализатор подписок для записи данных"""

    class Meta:
        fields = ('__all__')
        model = Subscription

    def validate(self, data):
        user = data.get('user')
        author = data.get('author')
        if user.subscriber.filter(author=author).exists():
            raise ValidationError(
                detail='Вы уже подписаны на данного автора',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data


class ShoppingCartReadSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок для чтения данных"""
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.CharField(source='recipe.cooking_time',
                                         read_only=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = ShoppingCart


class ShoppingCartWriteSerializer(serializers.ModelSerializer):
    """Сериализатор списка покупок для записи данных"""

    class Meta:
        fields = ('__all__')
        model = ShoppingCart

    def validate(self, data):
        user = data.get('user')
        recipe = data.get('recipe')
        if user.shopping_carts.filter(recipe=recipe).exists():
            raise serializers.ValidationError(
                'Данный рецепт уже добавлен в корзину')
        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор избранных рецептов"""

    class Meta:
        fields = ('__all__')
        model = Favorite

    def validate(self, data):
        user = data.get('user')
        recipe = data.get('recipe')
        if user.favorites.filter(recipe=recipe).exists():
            raise ValidationError(
                detail='Вы уже добавили данный рецепт',
                code=status.HTTP_400_BAD_REQUEST)
        if Recipe.objects.filter(pk=recipe.pk).count == 0:
            raise ValidationError(
                detail='Данного рецепта не существует',
                code=status.HTTP_400_BAD_REQUEST)
        return data
