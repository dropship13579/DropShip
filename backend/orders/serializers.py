# backend/orders/serializers.py
from decimal import Decimal
from rest_framework import serializers
from .models import Order, OrderItem
from accounts.models import Address


class OrderItemSerializer(serializers.ModelSerializer):
    product_slug = serializers.CharField(source="product.slug", read_only=True, default=None)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_slug",
            "product_name_snapshot",
            "product_image_snapshot",
            "unit_price",
            "quantity",
            "line_total",
        ]
        read_only_fields = fields


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    payment_method_display = serializers.CharField(source="get_payment_method_display", read_only=True)
    payment_status_display = serializers.CharField(source="get_payment_status_display", read_only=True)
    order_status_display = serializers.CharField(source="get_order_status_display", read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "shipping_address_snapshot",
            "subtotal",
            "shipping_fee",
            "coupon_code",
            "discount_amount",
            "total_amount",
            "payment_method",
            "payment_method_display",
            "payment_status",
            "payment_status_display",
            "order_status",
            "order_status_display",
            "tracking_number",
            "customer_notes",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = fields


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.IntegerField(required=True)
    payment_method = serializers.ChoiceField(
        choices=Order.PAYMENT_METHOD_CHOICES,
        default="cod"
    )
    coupon_code = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=50
    )
    customer_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
        max_length=1000
    )

    def validate_address_id(self, value):
        user = self.context["request"].user
        if not Address.objects.filter(id=value, user=user).exists():
            raise serializers.ValidationError("Selected address does not exist or does not belong to your account.")
        return value
