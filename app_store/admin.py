from django.contrib import admin
from app_store.models import *


class SpecValueInline(admin.TabularInline):
    model = Spec


class GalleryInline(admin.TabularInline):
    fk_name = "product"
    model = Gallery


class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "category",
        "description",
        "price",
        "stock",
        "created",
        "limited",
        "available",
        "purchases_num",
    ]

    search_fields = ["title"]
    inlines = [GalleryInline, SpecValueInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "parent", "icon", "image"]
    search_fields = ["name"]


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ["author", "product", "text", "created_at"]
    search_fields = ["author"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(Spec)
admin.site.register(SpecName)

