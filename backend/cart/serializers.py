# backend/cart/serializers.py
from rest_framework import serializers
from products.models import Product
from products.serializers import ProductListSerializer
from .models import Cart, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "unit_price",
            "line_total",
            "created_at",
            "updated_at",
        ]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "items",
            "total_items",
            "subtotal",
            "created_at",
            "updated_at",
        ]


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1, min_value=1)

    def validate_product_id(self, value):
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or is currently inactive.")
        return value

    def validate(self, data):
        product = Product.objects.get(id=data["product_id"])
        requested_qty = data.get("quantity", 1)

        if not product.is_in_stock:
            raise serializers.ValidationError({"product_id": f"'{product.name}' is currently out of stock."})

        if requested_qty > product.stock_quantity:
            raise serializers.ValidationError(
                {"quantity": f"Only {product.stock_quantity} units available in stock."}
            )

        data["product"] = product
        return data


class UpdateCartItemSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)

    def validate_quantity(self, value):
        cart_item = self.context.get("cart_item")
        if value > 0 and value > cart_item.product.stock_quantity:
            raise serializers.ValidationError(
                f"Only {cart_item.product.stock_quantity} units available in stock."
            )
        return value
