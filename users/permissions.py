from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором.
    """
    message = 'Отказано в доступе'

    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            request.user.groups.filter(name='Модераторы').exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """
    message = 'Отказано в доступе'

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False