import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipe_book.models import Recipe, Tag, Ingredient, Subscription, Favorite, \
    Shopping_cart, Structure

User = get_user_model()


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


class StructureSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = Structure
        fields = ('id', 'amount',)


class RecipeReadSerializer(serializers.ModelSerializer):
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
        request = self.context.get('request')
        user = request.user
        return Shopping_cart.objects.filter(recipe=obj, user=user).exists()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')
        read_only_fields = ('author', 'ingredients', 'tags',)
        lookup_field = 'name'


class RecipeWriteSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, many=False)
    ingredients = StructureSerializer(read_only=False, many=True)
    image = Base64ImageField(required=True, allow_null=False)

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            amount = int(ingredient.get('amount'))
            ingredient = get_object_or_404(Ingredient, pk=ingredient.get('id'))
            Structure.objects.create(recipe=recipe, ingredients=ingredient,
                                     amount=amount)

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError(
                'Мин. 1 ингредиент в рецепте!')
        return ingredients

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.set(tags)
        instance.ingredients.clear()
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance

    def to_representation(self, instance):
        return RecipeReadSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }).data

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'ingredients', 'name', 'image', 'text',
                  'cooking_time')


class IngredientSerializers(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()

    def get_measurement_unit(self, obj):
        return obj.get_measurement_unit_display()

    class Meta:
        model = Ingredient
        fields = ('__all__')


class SubscriptionSerializers(serializers.ModelSerializer):
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

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.author.recipes
        context = {'request': request}
        return RecipeReadSerializer(recipes, context=context, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    class Meta:
        model = Subscription
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name', 'recipes',
            'recipes_count')


class FavoriteSerializer(serializers.ModelSerializer):
    recipe = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        fields = ('recipe',)
        model = Favorite


class ShoppingCartSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='recipe.name', read_only=True)
    image = serializers.CharField(source='recipe.image', read_only=True)
    cooking_time = serializers.CharField(source='recipe.cooking_time',
                                         read_only=True)

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time')
        model = Shopping_cart
