from django.contrib import admin
from .models import Beat


@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "bpm", "price",)
    list_editable = ("price", )
    prepopulated_fields = {"url": ("name",)}

