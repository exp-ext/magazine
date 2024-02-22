from rest_framework import serializers
from products.models import Product, ProductsCategory, Manufacturer, Brand


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'


class ProductsCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductsCategory
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Manufacturer
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'
