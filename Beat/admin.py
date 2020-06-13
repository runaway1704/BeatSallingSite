from django.contrib import admin
from .models import Beat, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "url")
    prepopulated_fields = {"url": ("name",)}


@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "category", "price", "created", "updated",)
    list_filter = ("created", "updated",)
    list_editable = ("price", )
    prepopulated_fields = {"url": ("name",)}

