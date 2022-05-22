from django.contrib import admin
from .models import Category, Fandom, Product, Rating, RatingStar, Response


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)


class FandomAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Fandom, FandomAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "price", "stock", "available", "created", "updated"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Product, ProductAdmin)


class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "product", "ip")

admin.site.register(Rating, RatingAdmin)

admin.site.register(RatingStar)


class ResponseAdmin(admin.ModelAdmin):
    list_display = ["name", "comment", "active"]
    list_editable = ["active"]

admin.site.register(Response, ResponseAdmin)