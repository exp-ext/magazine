from addresses.models import Address, City, Country, Location, Region
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'latitude',
        'longitude',
        'ip_address',
        'timezone',
    )
    fieldsets = (
        ('Данные пользователя', {'fields': ('user', 'latitude', 'longitude', 'timezone')}),
        ('Последний вход', {'fields': ('ip_address',)}),
    )
    search_fields = ('user',)
    empty_value_display = '-пусто-'


@admin.register(Country)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class AddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    pass
