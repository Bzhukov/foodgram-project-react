import webcolors
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.utils.baseconv import base64
from rest_framework import serializers

from recipe_book.models import Recipe, Tag, Ingredient

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
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = AuthorSerializer(read_only=True, many=False)
    ingredients = IngredientSerializer(read_only=True, many=True)


    class Meta:
        fields = ('id', 'tags', 'author', 'ingredients','name','image', 'text', 'cooking_time')
        model = Recipe
        lookup_field = 'name'

class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')
