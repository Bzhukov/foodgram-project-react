import base64

import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipe_book.models import Recipe, Tag, Ingredient, Subscription, Favorite

User = get_user_model()


class Hex2NameColor(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            data = webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError('Для этого цвета нет имени')
        return data


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',)


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    def get_amount(self, obj):
        return obj.structure.first().amount

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'amount', 'measurement_unit',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True, many=False)
    ingredients = IngredientSerializer(read_only=True, many=True)
    image = Base64ImageField(required=True, allow_null=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        user = request.user
        return Favorite.objects.filter(recipe=obj, user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        return True

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'ingredients', 'tags',)
        lookup_field = 'name'


class IngredientSerializers(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()

    def get_measurement_unit(self, obj):
        return obj.get_measurement_unit_display()

    class Meta:
        model = Ingredient
        fields = ('__all__')


class SubscriptionSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email', read_only=True)
    id = serializers.PrimaryKeyRelatedField(source='author', read_only=True)
    username = serializers.CharField(source='author.username', read_only=True)
    first_name = serializers.CharField(source='author.first_name',
                                       read_only=True)
    last_name = serializers.CharField(source='author.last_name',
                                      read_only=True)
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.author.recipes
        context = {'request': request}
        return RecipeSerializer(recipes, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'recipes',
            'recipes_count')


class SubscriptionSerializers2(serializers.ModelSerializer):
    """Сериализатор подписки пользователя."""

    class Meta:
        model = Subscription
        fields = ('user_id', 'author_id')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.author.recipes
        context = {'request': request}
        return RecipeSerializer(recipes, context=context, many=True).data

    def validate(self, data):
        request = self.context.get('request')
        current_user = request.user
        author = self.initial_data['author']
        in_subscribed = Subscription.objects.filter(
            user=current_user,
            author=author
        )
        if request.method == 'POST':
            if in_subscribed.exists():
                raise serializers.ValidationError({
                    'errors': 'Вы уже подписаны на этого автора.'
                })
            if author == current_user:
                raise serializers.ValidationError({
                    'errors': 'Нельзя подписаться на себя.'
                })
        if request.method == 'DELETE':
            if not in_subscribed.exists():
                raise serializers.ValidationError({
                    'errors': 'Вы не подписаны на этого автора.'
                })
        return


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(many=False, read_only=True)


    class Meta:
        fields = ('recipe',)
        model = Favorite
