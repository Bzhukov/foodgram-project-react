from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from pytz import unicode
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from users.serializers import GetTokenSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """
    Получение токена в обмен на email и password.
    Права доступа: Доступно без токена.
    """
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        email=serializer.validated_data['email']
    )
    if user.check_password(serializer.validated_data['password']):
        access_token = Token.objects.get_or_create(user=user)
        print(access_token)
        # access_token = AccessToken.for_user(user)
        return Response(access_token,
                        status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    """
    Получение токена в обмен на email и password.
    Права доступа: Доступно без токена.
    """

    def post(self, request, *args, **kwargs):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User,
            email=serializer.validated_data['email']
        )
        if user.check_password(serializer.validated_data['password']):
            token, created = Token.objects.get_or_create(user=user)
            content = {
                'token': token.key,
            }
            return Response(content,
                        status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)