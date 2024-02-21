from django.contrib import admin

from attributes.models import Attribute, DataType, Unit


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(DataType)
class DataTypeAdmin(admin.ModelAdmin):
    pass
