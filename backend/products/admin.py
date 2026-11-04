# backend/products/admin.py
from django.contrib import admin
from .models import Product, ProductReview, WishlistItem, Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "contact_name",
        "email",
        "website_url",
        "average_shipping_days",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active", "created_at")
    search_fields = ("name", "contact_name", "email")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "supplier",
        "supplier_cost",
        "current_price",
        "original_price",
        "stock_quantity",
        "rating",
        "review_count",
        "is_active",
        "is_featured",
        "created_at",
    )
    list_filter = ("is_active", "is_featured", "category", "supplier", "created_at")
    search_fields = ("name", "description", "supplier_sku")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("supplier", "supplier_cost", "current_price", "stock_quantity", "is_active", "is_featured")


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "rating",
        "headline",
        "is_verified_purchase",
        "created_at",
    )
    list_filter = ("rating", "is_verified_purchase", "created_at")
    search_fields = ("product__name", "user__username", "headline", "comment")


@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "product__name")
    readonly_fields = ("created_at",)
