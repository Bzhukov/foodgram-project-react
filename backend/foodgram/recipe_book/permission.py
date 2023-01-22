from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Права на изменение и удаление разрешены только суперадмину."""
    message = 'Данное действие разрешено только администратору!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Права на изменение и удаление разрешены только суперадмину,
    или автору."""
    message = 'Данное действие разрешено СуперАдминистратору или автору'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(
            request.user.is_superuser
            or obj.author == request.user
        )
