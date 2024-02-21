from addresses.models import Address
from addresses.serializers import AddressSerializer
from django.db import IntegrityError
from rest_framework import serializers
from warehouses.models import Warehouse


class WarehouseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для складов.

    ### Attr:
    - address (AddressSerializer): Сериализатор для адреса склада.

    """
    address = AddressSerializer()

    class Meta:
        model = Warehouse
        fields = ('id', 'title', 'address', 'owner')
        read_only_fields = ('owner',)

    def _create_address(self, validated_data):
        address_data = validated_data.pop('address', None)
        try:
            address, _ = Address.objects.get_or_create(**address_data)
        except IntegrityError:
            raise serializers.ValidationError({'address': ['Not all required address fields are filled in.']})
        validated_data['address'] = address
        return validated_data

    def create(self, validated_data):
        validated_data = self._create_address(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data = self._create_address(validated_data)
        return super().update(instance, validated_data)
