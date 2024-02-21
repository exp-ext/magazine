from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'first_name': 'testuser_first_name',
            'last_name': 'testuser_last_name',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }

    def test_create_user(self):
        """
        Тест создания нового пользователя.
        """
        response = self.client.post('/api/v1/users/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            User.objects.filter(email=self.user_data['email']).exists()
        )

    def test_create_user_invalid_data(self):
        """
        Проверка того, что создание пользователя с недостоверными данными
        не удается.
        """
        invalid_user_data = [
            {
                'email': 'invalidemail@test.com',
                'password': 'testpassword'
            },
            {
                'first_name': 'testuser_first_name',
                'last_name': 'testuser_last_name',
                'email': 'testuser',
                'password': 'testpassword'
            },
        ]
        for data in invalid_user_data:
            response = self.client.post('/api/v1/users/', data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertFalse(
                User.objects.filter(
                    username=data['email']).exists()
            )
            if data == invalid_user_data[0]:
                self.assertTrue(
                    'This field is required.' in response.data['first_name']
                )

    def test_get_token(self):
        """
        Проверка получения token.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post('/api/v1/auth/token/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('auth_token' in response.data)

    def test_not_auth_logout(self):
        """
        Тест выхода из системы и аннулирование токена не авторизованным
        пользователем.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post('/api/v1/auth/token/logout/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logout(self):
        """
        Тест выхода из системы и аннулирование токена.
        """
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)
        response = self.client.post(
            '/api/v1/auth/token/logout/', HTTP_AUTHORIZATION=(
                f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(user=self.user).exists())