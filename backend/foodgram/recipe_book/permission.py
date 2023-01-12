from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permissions for change or delete Admin only"""
    message = 'Данное действие разрешено только администратору!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return bool(
            request.user and request.user.is_authenticated
            and (request.user.is_admin or request.user.is_superuser)
        )
