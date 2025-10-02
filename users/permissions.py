from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Отказано в доступе'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='Модераторы').exists()