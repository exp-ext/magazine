from addresses.models import Address, City, Country, Region
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from addresses.serializers import AddressSerializer

from ..models import Warehouse

User = get_user_model()


class WarehouseTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user, cls.admin_token = cls.create_user_and_token(is_staff=True)
        cls.normal_user, cls.normal_token = cls.create_user_and_token(is_staff=False)
        cls.country = Country.objects.create(title="Test Country")
        cls.region = Region.objects.create(country=cls.country, title="Test Region")
        cls.city = City.objects.create(region=cls.region, title="Test City")
        cls.address = Address.objects.create(
            city=cls.city,
            street='Тестовая улица',
            home=5,
            postcode='122896'
        )

    @classmethod
    def create_user_and_token(cls, is_staff):
        user = User.objects.create_user(
            email=f"{'admin' if is_staff else 'user'}@test.py",
            password='password',
            is_staff=is_staff,
            is_verified=True,
        )
        token, _ = Token.objects.get_or_create(user=user)
        return user, token.key

    def setUp(self):
        self.factory = APIRequestFactory()

        self.client = APIClient()

        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Token {self.normal_token}')

    def test_create_warehouse(self):
        # Проверка возможности создания склада
        address_serializer = AddressSerializer(self.address)
        post_data = {'title': 'Новый склад', 'address': address_serializer.data}
        response = self.user_client.post('/api/v1/warehouses/', post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Warehouse.objects.filter(title='Новый склад').exists())

    def test_warehouse_list(self):
        # Проверка получения списка складов
        response = self.admin_client.get('/api/v1/warehouses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_access(self):
        # Проверка отказа в доступе для неавторизованных пользователей
        self.client.logout()
        response = self.client.get('/api/v1/warehouses/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_warehouse(self):
        # Проверка обновления информации о складе
        warehouse = Warehouse.objects.create(title='Старый склад', address=self.address, owner=self.normal_user)
        response = self.user_client.patch(f'/api/v1/warehouses/{warehouse.id}/', {'title': 'Обновленный склад'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        warehouse.refresh_from_db()
        self.assertEqual(warehouse.title, 'Обновленный склад')

    def test_update_warehouse_address(self):
        # Проверка обновления адреса склада с созданием нового адреса
        address = Address.objects.create(
            city=self.city,
            street='Тестовая улица для теста',
            home=5,
            postcode='122896'
        )
        warehouse = Warehouse.objects.create(title='Старый склад', address=address, owner=self.normal_user)
        address_serializer = AddressSerializer(address).data
        address_data = {
            'street': 'новая улица',
            'home': '15',
            'postcode': '196358',
        }
        address_serializer.update(address_data)
        response = self.user_client.patch(f'/api/v1/warehouses/{warehouse.id}/', {'address': address_serializer}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        warehouse.refresh_from_db()
        address.refresh_from_db()
        self.assertEqual(warehouse.address.street, 'новая улица')
        self.assertTrue(Address.objects.filter(**address_data).exists())

    def test_delete_warehouse(self):
        # Проверка удаления склада
        warehouse = Warehouse.objects.create(title='Удаляемый склад', address=self.address, owner=self.normal_user)
        response = self.user_client.delete(f'/api/v1/warehouses/{warehouse.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Warehouse.objects.filter(id=warehouse.id).exists())
