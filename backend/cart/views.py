# backend/cart/views.py
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
)

def get_or_create_cart(request):
    """
    Returns the active cart for the authenticated user or current guest session.
    """
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # If there was an anonymous cart before login, merge it
        if request.session.session_key:
            anon_cart = Cart.objects.filter(session_key=request.session.session_key, user=None).first()
            if anon_cart:
                for item in anon_cart.items.all():
                    existing_item = CartItem.objects.filter(cart=cart, product=item.product).first()
                    if existing_item:
                        new_qty = existing_item.quantity + item.quantity
                        existing_item.quantity = min(new_qty, item.product.stock_quantity)
                        existing_item.save()
                    else:
                        item.cart = cart
                        item.save()
                anon_cart.delete()
        return cart
    else:
        if not request.session.session_key:
            request.session.save()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
        return cart


class CartDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart = get_or_create_cart(request)
        return Response(CartSerializer(cart).data)


class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        cart = get_or_create_cart(request)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            new_qty = cart_item.quantity + quantity
            if new_qty > product.stock_quantity:
                return Response(
                    {"quantity": f"Cannot add {quantity} more. Only {product.stock_quantity} available in stock."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            cart_item.quantity = new_qty
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class UpdateCartItemView(APIView):
    permission_classes = [permissions.AllowAny]

    def patch(self, request, pk):
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)

        serializer = UpdateCartItemSerializer(data=request.data, context={"cart_item": cart_item})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_quantity = serializer.validated_data["quantity"]

        if new_quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = new_quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class RemoveCartItemView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, pk):
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
        cart_item.delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        cart = get_or_create_cart(request)
        cart.items.all().delete()
        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
