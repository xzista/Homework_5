from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """
    Проверяет, что пользователь является модератором
    """

    message = "Отказано в доступе"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name="Модераторы").exists()


class IsNotModer(permissions.BasePermission):
    """
    Проверяет, что пользователь НЕ является модератором
    """

    message = "Модераторам запрещено это действие"

    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.groups.filter(name="Модераторы").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверяет, является ли пользователь владельцем.
    """

    message = "Отказано в доступе"

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class UserProfilePermission(permissions.BasePermission):
    """
    Разрешает:
    Просмотр любого профиля любому авторизованному пользователю
    Редактирование только своего профиля
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user