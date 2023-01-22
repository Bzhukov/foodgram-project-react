from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from users.serializers import GetTokenSerializer

User = get_user_model()


class CustomAuthToken(ObtainAuthToken):
    """
    Получение токена в обмен на email и password.
    Права доступа: Доступно без токена.
    """
    http_method_names = ['post', ]

    def post(self, request, *args, **kwargs):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            email=serializer.validated_data['email']
        )
        if user.check_password(serializer.validated_data['password']):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'auth_token': token.key, },
                            status=status.HTTP_200_OK)
        else:
            return Response({'password': 'Введен неверный пароль', },
                            status=status.HTTP_400_BAD_REQUEST)
