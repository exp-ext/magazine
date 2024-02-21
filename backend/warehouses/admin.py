from django.contrib import admin
from warehouses import models


@admin.register(models.Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'address',
        'owner',
    )
