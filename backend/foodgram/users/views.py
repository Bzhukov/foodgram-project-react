from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from users.permissions import IsAdmin
from users.serializers import GetTokenSerializer, UserEditSerializer

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
        refresh_token = RefreshToken.for_user(user)
        return Response({'token': str(access_token), 'refresh': str(refresh_token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """
    Получение списка всех пользователей.
    Права доступа: Администратор.
    Возможно получение и редактирование собственного профиля
    зарегестрированым пользователем по адресу 'me'
    """
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)

    @action(
        methods=['get'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @users_own_profile.mapping.patch
    def patch_own_profile(self, request):
        user = request.user
        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
#
