from core.pagination import CustomPaginator
from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from .serializers import SetPasswordSerializer

User = get_user_model()


class UserViewSet(UserViewSet):
    permission_classes = (DjangoModelPermissions,)
    pagination_class = CustomPaginator

    def perform_create(self, serializer: Serializer) -> None:
        """
        Создает нового пользователя и сохраняет его в базе данных.
        """
        serializer.is_valid(raise_exception=True)
        user = User.objects.create(**serializer.validated_data)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=('POST',), detail=False, permission_classes=(IsAuthenticated,))
    def set_password(self, request):
        serializer = SetPasswordSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({'detail': 'Пароль успешно изменен!'}, status=status.HTTP_204_NO_CONTENT)
