from django.contrib import admin
from .models import CarModel, CarMake


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 3


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["name", "make", "year", "type", "dealer_id"]


class CarMakeAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [CarModelInline]


# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
