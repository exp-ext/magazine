from addresses.models import Address, City, Country, Region
from rest_framework import serializers


class AddressSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Address.
    Сериализует информацию о адресах.

    """
    owner = serializers.ReadOnlyField(source='owner.id')

    class Meta:
        model = Address
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели City.
    Сериализует информацию о городах.

    """
    class Meta:
        model = City
        fields = '__all__'


class CountrySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Country.
    Сериализует информацию о странах.

    """
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Region.
    Сериализует информацию о регионах.

    """
    class Meta:
        model = Region
        fields = '__all__'
