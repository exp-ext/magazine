from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.db.models import Count, Max, Min, QuerySet, Sum
from django.db.models.deletion import CASCADE
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from addresses.models import Country
from attributes.models import Attribute
from fileflow.models import Image
from warehouses.models import Warehouse
from treebeard.mp_tree import MP_Node
from django.contrib.contenttypes.fields import GenericRelation

User = get_user_model()


class Brand(models.Model):
    """
    Модель для представления брендов.

    ### Args:
    - name (`str`): Название бренда.
    - image (ImageField, опционально): Фото бренда.

    """
    name = models.CharField(_('название бренда'), max_length=100)
    image = models.ForeignKey(Image, verbose_name=_('картинка'), related_name='brands', on_delete=CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = _('бренд')
        verbose_name_plural = _('бренды')

    def __str__(self):
        return f"{self.name}"


class Manufacturer(models.Model):
    """
    Модель для представления информации о производителях товаров.

    ### Args:
    - title (`str`): Наименование изготовителя товара.
    - brand (`Brand`): Изготавливаемый бренд, связанная с объектом модели Brand.
    - country (`Country`): Страна изготовления товара, связанная с объектом модели Country.

    """
    title = models.CharField(_('наименование изготовителя товара'), max_length=150)
    brand = models.ForeignKey(Brand, verbose_name=_('изготавливаемый бренд'), on_delete=models.CASCADE, related_name='manufacturers')
    country = models.ForeignKey(Country, verbose_name=_('страна изготовления'), on_delete=models.CASCADE, related_name='manufacturers')

    class Meta:
        verbose_name = _('производитель')
        verbose_name_plural = _('производители')

    def __str__(self):
        return f"{self.title}: {self.country}"


class ProductsCategory(MP_Node):
    """
    Модель для представления категорий товаров.

    ### Args:
    - category_name (`str`): Название категории.
    - image (`ImageField`, опционально): Фото категории.
    - parent_category (`ProductsCategory`, опционально): Родительская категория.

    ### Methods:
    - get_category_list(): Получает список категорий от текущей до корневой категории.
    - generate_filters(): Генерирует фильтры для категории, включая строки, числа и логические атрибуты.

    """
    node_order_by = ('id', )

    category_name = models.CharField('название', max_length=100)
    image = models.ForeignKey(Image, verbose_name=_('картинка'), related_name='product_categories', on_delete=CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return f"{self.category_name}"

    def get_category_list(self):
        category_list = []
        category_list.append(self)
        # for __ in range(self.level):
        #     category_list.append(category_list[len(category_list) - 1].parent_category)
        # category_list.reverse()
        return category_list


class Product(models.Model):
    """
    Модель для представления товаров в магазине.

    ### Args:
    - part_number (`str`): Артикул товара.
    - name (`str`): Название товара.
    - description (`str`, опционально): Описание товара.
    - brand (`Brand`): Бренд товара.
    - category (`ProductsCategory`, опционально): Категория товара.
    - length (`float`, опционально): Длина товара.
    - width (`float`, опционально): Ширина товара.
    - depth (`float`, опционально): Глубина товара.
    - weight (`float`, опционально): Вес товара.
    - manufacturer (`Manufacturer`, опционально): Производитель товара.
    - attributes (GenericRelation[Attribute]): Атрибуты товара.

    ### Methods:
    - get_warehouses_and_amount(): Получает информацию о складах и количестве товара.
    - get_amount_all(): Получает общее количество товара.
    - get_main_image(): Получает главное изображение товара.
    - get_alter_images(): Получает дополнительные изображения товара.
    - get_all_attributes(): Получает все атрибуты товара.
    - generate_url(): Генерирует URL для страницы товара.

    """
    part_number = models.CharField('артикул', max_length=100)
    name = models.CharField('название', max_length=100)
    description = models.TextField('описание', null=True, blank=True)

    brand = models.ForeignKey(Brand, verbose_name='бренд', related_name='products', on_delete=CASCADE)
    category = models.ForeignKey(ProductsCategory, verbose_name='категория', related_name='products', on_delete=CASCADE, null=True, blank=True)

    length = models.FloatField('длина', null=True, blank=True)
    width = models.FloatField('ширина', null=True, blank=True)
    depth = models.FloatField('глубина', null=True, blank=True)
    weight = models.FloatField('вес', null=True, blank=True)

    manufacturer = models.ForeignKey(Manufacturer, verbose_name='производитель', related_name='products', on_delete=CASCADE, null=True, blank=True)

    attributes = GenericRelation(Attribute, related_query_name='attributes', content_type_field='content_type', object_id_field='object_id')

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

    def __str__(self):
        return f"{self.name} ({self.part_number})"

    def get_warehouses_and_amount(self):
        stock = self.productunique_set.values('warehouse_id').order_by('warehouse_id').annotate(count=Count('warehouse_id'))
        stock_warehouse_list = []
        for stock_warehouse in stock:
            stock_warehouse_list.append({
                'count': stock_warehouse['count'],
                'warehouse_address': str(get_object_or_404(Warehouse, id=stock_warehouse['warehouse_id']).address),
            })
        return stock_warehouse_list

    def get_amount_all(self):
        return len(self.stocked_products.all())

    def get_main_image(self):
        img = self.images.all().filter(is_first=True).first()
        return img.image.image_webp.url if img else None

    def get_alter_images(self):
        return self.images.all().filter(is_first=False)

    def set_attribute(self, attr_name, attr_value, attr_category):
        """Метод добавления атрибута.

        ### Args:
        - attr_name (`str`): Название атрибута.
        - attr_value (`str`): Строка со значением атрибута. Парсится на `int|float+ЕИ` или возвращает str если не найдено числа.
        - attr_category (`str`, опционально): Название категории атрибута.

        """
        Attribute().add_attribute_to_model(
            initial_instance=self,
            attr_name=attr_name,
            attr_value=attr_value,
            attr_category=attr_category
        )
        return self
