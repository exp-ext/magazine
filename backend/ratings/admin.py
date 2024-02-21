from django.contrib import admin
from ratings.models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
