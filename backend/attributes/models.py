import re

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Model, UniqueConstraint
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from rest_framework.exceptions import ValidationError


class AttrCategory(models.Model):
    """
    Модель для категорий атрибутов.

    ### Fields:
    - name (`CharField`): Название категории.

    ### Meta:
    - constraints (`list`): Ограничения на модель.
        - UniqueConstraint: Уникальное ограничение на поле `name`.

    """
    name = models.CharField(max_length=100)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['name'], name='unique_name')
        ]

    def __str__(self):
        return self.name


class StrTypeChoice(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Unit(models.Model):
    """
    Модель для представления единиц измерения.

    ### Fields:
    - name (`str`): Название единицы измерения.
    - name_many (`str`): Название множественного числа единицы измерения.
    - symbol (`str`): Символ единицы измерения.

    """
    name = models.CharField(_('название ЕИ'), max_length=100, unique=True)
    name_many = models.CharField(_('название множественного числа ЕИ'), max_length=100, unique=True)
    symbol = models.CharField(_('символ ЕИ'), max_length=5, unique=True)

    class Meta:
        verbose_name = _('единица измерения')
        verbose_name_plural = _('единицы измерения')

    def __str__(self):
        return f'{self.name} - {self.symbol}'


class DataType(PolymorphicModel):
    """
    Базовая модель для типов данных.

    ### Fields:
    - name (`CharField`): Название типа данных.

    ### Methods:
    - __str__(): Возвращает строковое представление объекта.
    - parse_value_get_or_create(data_type_name, data_type_value): Статический метод для разбора значения атрибута и создания или получения объекта типа данных.
    - parse_value(input_string, params): Статический метод для разбора значения атрибута.

    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @staticmethod
    def parse_value_get_or_create(data_type_name, data_type_value):
        """
        Статический метод для разбора значения атрибута и создания или получения объекта типа данных.

        ### Args:
        - data_type_name (`str`): Название типа данных.
        - data_type_value (`str`): Строка со значениями типа данных.

        ### Returns:
        - `DataType`: Созданный или полученный объект типа данных.

        """
        params = {
            'poly_model': None,
            'name': data_type_name,
        }

        params = DataType.parse_value(data_type_value, params)

        poly_model = params.pop('poly_model')
        str_type_choice_instance = params.pop('choice', None)

        instance, _ = poly_model.objects.get_or_create(**params)

        if str_type_choice_instance:
            instance.value.set((str_type_choice_instance,))

        return instance

    @staticmethod
    def parse_value(input_string: str, params: dict) -> dict:
        """
        Статический метод для разбора значения атрибута.

        ### Args:
        - input_string (`str`): Входная строка для разбора.
        - params (`dict`): Словарь с общими параметрами.

        ### Returns:
        - `dict`: Обновленный словарь с параметрами.

        """
        input_string = input_string.replace(',', '.').lower()

        float_or_int_with_unit_pattern = re.compile(r'(?P<number>\d+(?:\.\d+)?)(\s*)(?P<unit>[a-zA-ZА-Яа-я]*)$')
        bool_pattern = re.compile(r'^(да|есть|нет)$', re.IGNORECASE)
        match = float_or_int_with_unit_pattern.match(input_string)

        if match:
            number = match.group('number')
            unit = match.group('unit')
            if '.' in number:
                poly_model, value = FloatType, float(number)
            else:
                poly_model, value = IntType, int(number)

            if len(unit) > 2:
                unit_instance = Unit.objects.filter(name__icontains=unit, name_many__icontains=unit).first()
            else:
                unit_instance = Unit.objects.filter(name__icontains=unit, name_many__icontains=unit, symbol__iexact=unit).first()

            params.update({
                'poly_model': poly_model,
                'value': value,
                **({'unit': unit_instance} if unit_instance else {})
            })
        elif bool_pattern.match(input_string.lower()):
            params.update({
                'poly_model': BoolType,
                'value': input_string.lower() in ('да', 'есть'),
            })
        else:
            string_instance = StrTypeChoice.objects.filter(name__icontains=input_string).first()
            if not string_instance:
                string_instance = StrTypeChoice.objects.create(name=input_string)

            params.update({
                'poly_model': StrType,
                'choice': string_instance,
            })
        return params


class StrType(DataType):
    """
    Модель для строкового типа данных.

    ### Fields:
    - value (`ManyToManyField[StrTypeChoice]`): Значение типа данных.

    """
    value = models.ManyToManyField(StrTypeChoice, related_name='str_types', blank=True)

    def __str__(self):
        return self.name


class IntType(DataType):
    """
    Модель для целочисленного типа данных.

    ### Fields:
    - value (`IntegerField`): Значение типа данных.
    - unit (`ForeignKey[Unit]`, опционально): Единица измерения.

    """
    value = models.IntegerField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='единица измерения', null=True, blank=True)


class FloatType(DataType):
    """
    Модель для вещественного типа данных.

    ### Fields:
    - value (`FloatField`): Значение типа данных.
    - unit (`ForeignKey[Unit]`, опционально): Единица измерения.

    """
    value = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name='единица измерения', null=True, blank=True)


class BoolType(DataType):
    """
    Модель для логического типа данных.

    ### Fields:
    - value (`BooleanField`): Значение типа данных.

    """
    value = models.BooleanField()


class Attribute(models.Model):
    """
    Модель для представления атрибутов товаров.

    ### Fields:
    - category (`ForeignKey[AttrCategory]`): Категория атрибута.
    - data_type (`ForeignKey[DataType]`): Тип данных атрибута.

    - content_type (`ForeignKey[ContentType]`): Тип содержимого для обобщенной связи.
    - object_id (`PositiveIntegerField`): Идентификатор объекта для обобщенной связи.
    - content_object (`GenericForeignKey`): Обобщенная связь с объектом.
    """

    category = models.ForeignKey(AttrCategory, on_delete=models.CASCADE, verbose_name=_('категория атрибута'), null=True, blank=True)
    data_type = models.ForeignKey(DataType, on_delete=models.CASCADE, verbose_name=_('тип данных'))

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'атрибут'
        verbose_name_plural = 'атрибуты'

    def __str__(self):
        return f'{self.id} | {self.category}'

    def add_attribute_to_model(self, initial_instance: Model, attr_name: str, attr_value: str, attr_category: str = None):
        """Метод для добавления атрибута к модели.

        ### Args:
        - initial_instance (`Model`): Экземпляр модели к которой добавляется атрибут.
        - attr_name (`str`): Название атрибута.
        - attr_value (`str`): Строка со значением атрибута. Парсится на `int|float+ЕИ` или возвращает str если не найдено числа.
        - attr_category (`str`, опционально): Название категории атрибута.

        ### Raises:
        - ValidationError: Если переданный экземпляр не является экземпляром модели Django.

        ### Returns:
        - `Attribute`: Созданный атрибут.

        """
        if not isinstance(initial_instance, Model):
            raise ValidationError('Переданный экземпляр не является экземпляром модели Django.')

        content_type = ContentType.objects.get_for_model(initial_instance)

        if attr_category:
            category_instance, _ = AttrCategory.objects.get_or_create(name=attr_category)

        data_type_instance = DataType.parse_value_get_or_create(attr_name, attr_value)

        return Attribute.objects.create(
            content_type=content_type,
            object_id=initial_instance.id,
            category=category_instance,
            data_type=data_type_instance,
        )
