from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()


class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'first_name': 'testuser_first_name',
            'last_name': 'testuser_last_name',
            'email': 'testuser@test.com',
            'password': 'testpassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.token = Token.objects.create(user=self.user)

    def test_get_users(self):
        """
        Тест получения списка пользователей.
        """
        response = self.client.get(
            '/api/v1/users/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_profile(self):
        """
        Тест получения профиля пользователя.
        """
        response = self.client.get(
            f'/api/v1/users/{self.user.id}/',
            HTTP_AUTHORIZATION=(f'Token {self.token.key}')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_not_get_user_profile(self):
        """
        Тест неполучения профиля пользователя.
        """
        response = self.client.get(
            f'/api/v1/users/{self.user.id}/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_current_user(self):
        """
        Тест получения текущего пользователя.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/v1/users/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_not_set_password(self):
        """
        Проверка неправильного изменения пароля пользователя.
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = [
            {
                'new_password': 'testpassword',
                'current_password': 'testpassword'
            },
            {
                'new_password': 'newtestpassword1',
            },
        ]
        for password in new_password_data:
            response = self.client.post(
                '/api/v1/users/set_password/', password
            )
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            if password == new_password_data[1]:
                self.assertTrue(
                    ('This field is required.'
                        in response.data['current_password'])
                )

    def test_set_password(self):
        """
        Проверка изменения пароля пользователя.
        """
        self.client.force_authenticate(user=self.user)
        new_password_data = {
            'new_password': 'newtestpassword1',
            'current_password': 'testpassword'
        }
        response = self.client.post(
            '/api/v1/users/set_password/', new_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            self.user.check_password(new_password_data['current_password'])
        )
        self.assertTrue(
            self.user.check_password(new_password_data['new_password'])
        )

    def test_not_auth_set_password(self):
        """
        Проверка изменения пароля неавторизованным пользователем.
        """
        new_password_data = {
            'new_password': 'newtestpassword1',
            'current_password': 'testpassword'
        }
        response = self.client.post(
            '/api/v1/users/set_password/', new_password_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
