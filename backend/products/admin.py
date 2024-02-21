from django.contrib import admin

from products.models import Product, ProductsCategory, Manufacturer, Brand


@admin.register(ProductsCategory)
class ProductsCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
