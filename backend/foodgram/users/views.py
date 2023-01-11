from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken


from users.serializers import GetTokenSerializer

User = get_user_model()
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_jwt_token(request):
    """
    Получение JWT-токена в обмен на email и password.
    Права доступа: Доступно без токена.
    """
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        email=serializer.validated_data['email']
    )
    if user.check_password(serializer.validated_data['password']):
        access_token = AccessToken.for_user(user)
        return Response({'token': str(access_token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)