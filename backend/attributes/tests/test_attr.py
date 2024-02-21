from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

from ..models import (AttrCategory, Attribute, BoolType, DataType, FloatType,
                      IntType, StrType, Unit)


class AttributeModelTest(TestCase):

    def setUp(self):
        self.category = AttrCategory.objects.create(name="Тестовая категория")
        self.unit_m = Unit.objects.create(name="метр", name_many="метры", symbol="м")
        self.unit_A = Unit.objects.create(name="Ампер", name_many="амперы", symbol="А")
        self.unit_Wt = Unit.objects.create(name="ватт", name_many="ватты", symbol="Вт")

    def test_parse_value_get_or_create(self):
        # Тестирование создания DataType с разными типами данных
        str_instance = DataType.parse_value_get_or_create("Строка", "тестовое значение")
        self.assertIsInstance(str_instance, StrType)

        int_instance = DataType.parse_value_get_or_create("Целое", "123")
        self.assertIsInstance(int_instance, IntType)
        self.assertEqual(int_instance.value, 123)
        self.assertIsNone(int_instance.unit)

        int_instance = DataType.parse_value_get_or_create("Целое в метрах", "12м")
        self.assertIsInstance(int_instance, IntType)
        self.assertEqual(int_instance.value, 12)
        self.assertEqual(int_instance.unit, self.unit_m)

        int_instance = DataType.parse_value_get_or_create("Целое в метрах с Б", "12 Метр")
        self.assertIsInstance(int_instance, IntType)
        self.assertEqual(int_instance.value, 12)
        self.assertEqual(int_instance.unit, self.unit_m)

        int_instance = DataType.parse_value_get_or_create("Целое в амперах", "12ампер")
        self.assertIsInstance(int_instance, IntType)
        self.assertEqual(int_instance.value, 12)
        self.assertEqual(int_instance.unit, self.unit_A)

        float_instance = DataType.parse_value_get_or_create("Вещественное", "123.45")
        self.assertIsInstance(float_instance, FloatType)
        self.assertEqual(float_instance.value, 123.45)

        float_instance = DataType.parse_value_get_or_create("Вещественное", "123.45метр")
        self.assertIsInstance(float_instance, FloatType)
        self.assertEqual(float_instance.value, 123.45)
        self.assertEqual(float_instance.unit, self.unit_m)

        float_instance = DataType.parse_value_get_or_create("Вещественное в амперах", "123.45А")
        self.assertIsInstance(float_instance, FloatType)
        self.assertEqual(float_instance.value, 123.45)
        self.assertEqual(float_instance.unit, self.unit_A)

        bool_instance = DataType.parse_value_get_or_create("Булево", "да")
        self.assertIsInstance(bool_instance, BoolType)
        self.assertTrue(bool_instance.value)

        bool_instance = DataType.parse_value_get_or_create("Булево", "есть")
        self.assertIsInstance(bool_instance, BoolType)
        self.assertTrue(bool_instance.value)

        bool_instance = DataType.parse_value_get_or_create("Булево", "нет")
        self.assertIsInstance(bool_instance, BoolType)
        self.assertFalse(bool_instance.value)

    def test_add_attribute_to_model(self):
        test_product = ContentType.objects.create(model='testproduct')

        # Проверяем добавление атрибута к модели
        attribute_instance = Attribute().add_attribute_to_model(
            initial_instance=test_product,
            attr_name="Тестовый атрибут",
            attr_value="тестовое значение",
            attr_category="Тестовая категория"
        )
        self.assertIsInstance(attribute_instance, Attribute)
        self.assertEqual(attribute_instance.category.name, "Тестовая категория")
        self.assertEqual(attribute_instance.data_type.name, "Тестовый атрибут")
        self.assertEqual(attribute_instance.data_type.value.first().name, "тестовое значение")
        self.assertIsInstance(attribute_instance.data_type, StrType)
        self.assertIs(test_product.attribute_set.exists(), False)
