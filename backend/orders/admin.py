# backend/orders/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name_snapshot", "unit_price", "quantity", "line_total")
    can_delete = False


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "min_order_amount",
        "used_count",
        "usage_limit",
        "is_active",
        "valid_until",
        "created_at",
    )
    list_filter = ("discount_type", "is_active", "created_at")
    search_fields = ("code",)
    readonly_fields = ("used_count", "created_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "total_amount",
        "coupon_code",
        "discount_amount",
        "payment_method",
        "payment_status",
        "order_status",
        "tracking_number",
        "created_at",
    )
    list_filter = ("order_status", "payment_status", "payment_method", "created_at")
    search_fields = ("order_number", "user__username", "user__email", "tracking_number", "coupon_code")
    readonly_fields = (
        "order_number",
        "user",
        "shipping_address_snapshot",
        "subtotal",
        "shipping_fee",
        "coupon_code",
        "discount_amount",
        "total_amount",
        "created_at",
        "updated_at",
    )
    inlines = [OrderItemInline]
    ordering = ("-created_at",)
