import pytz
from core.models import Create
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Location(Create):
    """
    Модель Location представляет информацию о местоположении пользователя, включая координаты широты и долготы,
    IP-адрес и часовой пояс.

    ### Attributes:
    - user (`ForeignKey`): Ссылка на пользователя, к которому относится данное местоположение (related_name='locations').
    - latitude (`FloatField`): Широта местоположения.
    - longitude (`FloatField`): Долгота местоположения.
    - ip_address (`CharField`): IP-адрес, связанный с этим местоположением.
    - timezone (`CharField`): Часовой пояс местоположения, выбранный из доступных вариантов в TIMEZONES.

    """
    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()

    ip_address = models.CharField(_('IP адрес'), max_length=100)

    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='Europe/Moscow')

    class Meta:
        verbose_name = _('координаты')
        verbose_name_plural = _('координаты')

    def __str__(self):
        return self.user


class Country(models.Model):
    """
    Модель для представления информации о странах.

    ### Attributes:
    - name (str): Название страны.

    """
    title = models.CharField("Название страны", max_length=100)

    class Meta:
        verbose_name = _("страна")
        verbose_name_plural = _("страны")

    def __str__(self):
        return self.title


class Region(models.Model):
    """
    Модель Region представляет информацию о регионах (областях) внутри страны. Каждый регион связан с определенной
    страной и имеет название, которое может быть пустым (например, для стран без деления на области).

    ### Attributes:
    - country (`ForeignKey`): Ссылка на страну, к которой относится данный регион (related_name='regions').
    - title (`CharField`): Название региона (области).

    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="regions", verbose_name="Страна")
    title = models.CharField("Область", max_length=100)

    class Meta:
        verbose_name = _("регион")
        verbose_name_plural = _("регионы")

    def __str__(self):
        region = f'{self.country}'
        region += f', {self.title}' if self.title else ''
        return region


class City(models.Model):
    """
    Модель City представляет информацию о населенных пунктах внутри региона (области). Каждый населенный пункт
    связан с определенным регионом и имеет название.

    ### Attributes:
    - region (`ForeignKey`): Ссылка на регион, к которому относится данный населенный пункт (related_name='cities').
    - title (`CharField`): Название населенного пункта.

    """
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="cities", verbose_name="Регион")
    title = models.CharField("Город", max_length=100)

    class Meta:
        verbose_name = "Населённый пункт"
        verbose_name_plural = "Населённые пункты"

    def __str__(self):
        return f"{self.title}"


class Address(models.Model):
    """
    Модель Address представляет информацию об адресе, включая улицу, номер дома, корпус, офис/квартиру, примечание и индекс.

    ### Attributes:
    - city (ForeignKey): Ссылка на город, к которому относится адрес (related_name='addresses').
    - street (CharField): Название улицы.
    - home (CharField): Номер дома.
    - building (CharField, optional): Корпус (если применимо).
    - apartment (CharField, optional): Офис или квартира (если применимо).
    - note (TextField, optional): Примечание (дополнительная информация).
    - postcode (CharField, optional): Индекс (если применимо).

    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(_('название улицы'), max_length=100)
    home = models.CharField(_('номер дома'), max_length=20)
    building = models.CharField(_('корпус'), max_length=20, blank=True, null=True)
    liter = models.CharField(_('литер'), max_length=3, blank=True, null=True)
    apartment = models.CharField(_('офис/квартира'), max_length=20, blank=True, null=True)
    note = models.TextField(_('примечание'), blank=True, null=True)
    postcode = models.CharField(_('индекс'), max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = _('адрес')
        verbose_name_plural = _('адреса')

    def __str__(self):
        address = f'{self.city}, ул. {self.street}, дом {self.home}'
        if self.building:
            address += f', корп. {self.building}'
        if self.apartment:
            address += f', офис {self.apartment}'
        if self.postcode:
            address += f' ({self.postcode})'
        return address
