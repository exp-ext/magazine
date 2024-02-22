from addresses.models import Country
from attributes.models import StrType
from django.test import TestCase

from ..models import Attribute, Brand, Manufacturer, Product, ProductsCategory


class ProductModelTest(TestCase):
    def setUp(self):
        country = Country.objects.create(title="Test Country")
        self.brand = Brand.objects.create(title="Test Brand")
        self.product_category = ProductsCategory.add_root(category_name="Test ProductsCategory")
        self.manufacturer = Manufacturer.objects.create(brand=self.brand, title="Test Manufacturer", country=country)

    def test_add_attribute_to_model(self):
        test_product = Product.objects.create(
            part_number='118935rh-po',
            title='test name',
            description='test описание' * 10,
            brand=self.brand,
            category=self.product_category,
            length=58.5,
            width=28.6,
            depth=85,
            weight=96,
            manufacturer=self.manufacturer
        )

        attr_name = "Тестовый атрибут"
        attr_value = "тестовое значение"
        attr_category = "Тестовая категория"

        test_product.set_attribute(attr_name, attr_value, attr_category)

        attribute_instance = test_product.attributes.last()

        self.assertIsInstance(attribute_instance, Attribute)
        self.assertEqual(attribute_instance.category.name, "Тестовая категория")
        self.assertEqual(attribute_instance.data_type.name, "Тестовый атрибут")
        self.assertEqual(attribute_instance.data_type.value.first().name, "тестовое значение")
        self.assertIsInstance(attribute_instance.data_type, StrType)
