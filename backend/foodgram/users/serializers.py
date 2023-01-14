from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


# class CustomUserSerializer(UserSerializer):
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'first_name', 'last_name')

class GetTokenSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            'email', 'password'
        )
