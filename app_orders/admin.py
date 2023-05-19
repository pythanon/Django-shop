from django.contrib import admin

from .models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "profile",
        "address",
        "delivery_type",
        "delivery_price",
        "city",
        "paid",
        "created",
        "updated",
        "payment_type",
    ]
    list_filter = ["paid", "created", "updated"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
