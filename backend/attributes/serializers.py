from rest_framework import serializers

from attributes.models import Attribute, DataType, Unit


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = '__all__'


class DataTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataType
        fields = '__all__'


class AttributeSerializer(serializers.ModelSerializer):
    data_type = serializers.SlugRelatedField(slug_field='name', queryset=DataType.objects.all(), allow_null=False)

    class Meta:
        model = Attribute
        fields = '__all__'
