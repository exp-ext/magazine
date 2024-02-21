from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAdmin(BasePermission):
    """
    Права доступа: Администратор.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return request.user.is_authenticated and request.user.is_admin


class IsModerator(BasePermission):
    """
    Права доступа: Модератор.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BasePermission):
    """
    Права доступа: Чтение.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in SAFE_METHODS

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    Права доступа: Владелец.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return request.user and request.user == obj.owner


class IsAdminOrReadOnly(BasePermission):
    """
    Объединение разрешений IsAdmin и ReadOnly.
    """

    def has_permission(self, request, view):
        return IsAdmin().has_permission(request, view) or ReadOnly().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return IsAdmin().has_object_permission(request, view, obj) or ReadOnly().has_object_permission(request, view, obj)


class IsModeratorOrReadOnly(BasePermission):
    """
    Объединение разрешений IsModerator и ReadOnly.
    """

    def has_permission(self, request, view):
        return IsModerator().has_permission(request, view) or ReadOnly().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return IsModerator().has_object_permission(request, view, obj) or ReadOnly().has_object_permission(request, view, obj)


class IsOwnerOrReadOnly(BasePermission):
    """
    Объединение разрешений IsOwner и ReadOnly.
    """

    def has_permission(self, request, view):
        return IsOwner().has_permission(request, view) or ReadOnly().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return IsOwner().has_object_permission(request, view, obj) or ReadOnly().has_object_permission(request, view, obj)
