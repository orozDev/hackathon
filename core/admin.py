from django.contrib import admin

from core.models import City, Service


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    readonly_fields = ('created_at', 'updated_at',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('id', 'name',)
    search_fields = ('id', 'name',)
    readonly_fields = ('created_at', 'updated_at',)

# Register your models here.
