from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


class OrderItemTabular(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("email", "paid", 'created',)
    readonly_fields = ("email", "paid", "created",)
    list_filter = ("paid",)
    inlines = [OrderItemTabular]