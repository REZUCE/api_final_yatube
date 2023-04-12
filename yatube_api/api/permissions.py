from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    # В этом методе проверяется, является ли метод запроса безопасным
    # (GET, HEAD, OPTIONS), и если да, то вернется True, чтобы разрешить
    # любому пользователю просматривать объект.
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)
