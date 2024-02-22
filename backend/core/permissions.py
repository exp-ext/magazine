from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAuthenticated(BasePermission):
    """
    Доступ разрешен только аутентифицированным пользователям.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)


class IsAdmin(BasePermission):
    """
    Права доступа: Администратор.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.user.is_authenticated and request.user.is_admin)

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return self.has_permission(request, view)


class IsModerator(BasePermission):
    """
    Права доступа: Модератор.
    """

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_moderator)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReadOnly(BasePermission):
    """
    Права доступа: Чтение.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.method in SAFE_METHODS)

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return self.has_permission(request, view)


class IsOwner(BasePermission):
    """
    Права доступа: Владелец.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return bool(request.method in SAFE_METHODS or request.user.is_authenticated and request.user.is_verified)

    def has_object_permission(self, request: Request, view: View, obj: Model) -> bool:
        return bool(request.user.is_authenticated and request.user == obj.owner)
