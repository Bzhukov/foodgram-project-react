from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name')


class GetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'email', 'password'
        )

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True,
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        lookup_field = 'email'
        fields = ('username', 'email', 'first_name', 'last_name',)
        model = User


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        lookup_field = 'username'
        fields = ('username', 'email', 'first_name', 'last_name', )
        model = User


