from addresses.models import Address
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _
from warehouses.models import Warehouse

User = get_user_model()


class Outlet(models.Model):
    """
    Модель для представления магазинов.

    ### Поля:
    - title (`CharField`): Название магазина.
    - address (`ForeignKey[Address]`): Адрес магазина.
    - warehouses (`ManyToManyField[Warehouse]`): Склады магазина.
    - owner (`ForeignKey[User]`): Владелец магазина.

    ### Meta:
    - constraints (`tuple`): Ограничения уникальность 'title' и 'address'.

    """
    title = models.CharField(_('название магазина'), max_length=150, unique=True)
    address = models.ForeignKey(Address, verbose_name=_('адрес'), related_name='outlets', on_delete=CASCADE)
    warehouses = models.ManyToManyField(Warehouse, related_name='outlets', verbose_name="Склады")

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='outlets')

    class Meta:
        verbose_name = "магазин"
        verbose_name_plural = "магазины"
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'address'),
                name='\n%(app_label)s_%(class)s_title_address_unique'
            ),
        )

    def __str__(self):
        return f"Магазин {self.title} ({self.address})"
