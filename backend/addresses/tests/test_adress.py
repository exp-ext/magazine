import unittest

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APIRequestFactory

from ..models import City, Country, Region
from ..serializers import CitySerializer, CountrySerializer, RegionSerializer
from ..views import CityViewSet, CountryViewSet, RegionViewSet

User = get_user_model()


class TestCityModel(unittest.TestCase):
    def setUp(self):
        country = Country.objects.create(title="Test Country")
        region = Region.objects.create(country=country, title="Test Region")
        self.city = City.objects.create(region=region, title="Test City")

    def test_city_str(self):
        self.assertEqual(str(self.city), "Test City")


class TestCountryModel(unittest.TestCase):
    def setUp(self):
        self.country = Country.objects.create(title="Test Country")

    def test_country_str(self):
        self.assertEqual(str(self.country), "Test Country")


class TestRegionModel(unittest.TestCase):
    def setUp(self):
        self.country = Country.objects.create(title="Test Country")
        self.region = Region.objects.create(country=self.country, title="Test Region")
        self.region_without_title = Region.objects.create(country=self.country)

    def test_region_str(self):
        self.assertEqual(str(self.region), "Test Country, Test Region")
        self.assertEqual(str(self.region_without_title), "Test Country")


class TestCitySerializer(unittest.TestCase):
    def test_city_serializer(self):
        country = Country.objects.create(title="Test Country")
        region = Region.objects.create(country=country, title="Test Region")
        city_data = {"title": "Test City", "region": region.id}
        serializer = CitySerializer(data=city_data)
        self.assertTrue(serializer.is_valid())


class TestCountrySerializer(unittest.TestCase):
    def test_country_serializer(self):
        country_data = {"title": "Test Country"}
        serializer = CountrySerializer(data=country_data)
        self.assertTrue(serializer.is_valid())


class TestRegionSerializer(unittest.TestCase):
    def test_region_serializer(self):
        country = Country.objects.create(title="Test Country")
        region_data = {"country": country.id, "title": "Test Region"}
        serializer = RegionSerializer(data=region_data)
        self.assertTrue(serializer.is_valid())


class TestCityViewSet(unittest.TestCase):
    def test_city_viewset(self):
        factory = APIRequestFactory()
        request = factory.get("/api/v1/cities/")
        view = CityViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)


class TestCountryViewSet(unittest.TestCase):
    def test_country_viewset(self):
        factory = APIRequestFactory()
        request = factory.get("/api/v1/countries/")
        view = CountryViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)


class TestRegionViewSet(unittest.TestCase):
    def test_region_viewset(self):
        factory = APIRequestFactory()
        request = factory.get("/api/v1/regions/")
        view = RegionViewSet.as_view({"get": "list"})
        response = view(request)
        self.assertEqual(response.status_code, 200)


class PermissionsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.admin_user, cls.admin_token = cls.create_user_and_token(is_staff=True)
        cls.normal_user, cls.normal_token = cls.create_user_and_token(is_staff=False)
        cls.country = Country.objects.create(title="Test Country")
        cls.region = Region.objects.create(country=cls.country, title="Test Region")
        cls.city = City.objects.create(region=cls.region, title="Test City")

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

        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token}')

        self.user_client = APIClient()
        self.user_client.credentials(HTTP_AUTHORIZATION=f'Token {self.normal_token}')

    def test_city_viewset_permissions(self):
        # Test access for admin user
        response = self.admin_client.get("/api/v1/addresses/cities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {"region": self.region.id, "title": "New City"}
        response = self.admin_client.post("/api/v1/addresses/cities/", post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test access for normal user
        response = self.user_client.get("/api/v1/addresses/cities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.post("/api/v1/addresses/cities/", post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_country_viewset_permissions(self):
        # Test access for admin user
        response = self.admin_client.get("/api/v1/addresses/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {"title": "New Country"}
        response = self.admin_client.post("/api/v1/addresses/countries/", post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test access for normal user
        response = self.user_client.get("/api/v1/addresses/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.post("/api/v1/addresses/countries/", post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_region_viewset_permissions(self):
        # Test access for admin user
        response = self.admin_client.get("/api/v1/addresses/regions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        post_data = {"country": self.country.id, "title": "New Region"}
        response = self.admin_client.post("/api/v1/addresses/regions/", post_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test access for normal user
        response = self.user_client.get("/api/v1/addresses/regions/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.user_client.post("/api/v1/addresses/regions/", post_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
