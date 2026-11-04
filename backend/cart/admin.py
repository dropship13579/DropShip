# backend/cart/admin.py
from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ["product", "quantity", "unit_price", "line_total"]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "__str__", "total_items", "subtotal", "updated_at"]
    inlines = [CartItemInline]
