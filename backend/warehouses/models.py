from addresses.models import Address
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Warehouse(models.Model):
    """
    Модель для представления складов.

    ### Args:
    - title(CharField): Название склада.
    - address (Address): Адрес склада.
    - owner(User): Владелец склада.

    """
    title = models.CharField(_("название склада"), max_length=150, unique=True)
    address = models.ForeignKey(Address, verbose_name=_("адрес"), related_name="warehouses", on_delete=CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warehouses')

    class Meta:
        verbose_name = "склад"
        verbose_name_plural = "склады"
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'address'),
                name='\n%(app_label)s_%(class)s_title_address_unique'
            ),
        )

    def __str__(self):
        return f"Склад {self.title} ({self.address})"
