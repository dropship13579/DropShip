# backend/orders/views.py
from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Address
from cart.views import get_or_create_cart
from .models import Order, OrderItem, Coupon
from .serializers import OrderSerializer, CheckoutSerializer


class CouponValidateView(APIView):
    """
    POST /api/orders/coupons/validate/
    Validates a coupon code against a subtotal or current active cart items.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        code = request.data.get("code", "").strip().upper()
        if not code:
            return Response(
                {"detail": "Please enter a promotional coupon code."},
                status=status.HTTP_400_BAD_REQUEST
            )

        coupon = Coupon.objects.filter(code__iexact=code).first()
        if not coupon:
            return Response(
                {"detail": f"Coupon '{code}' does not exist or is invalid."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Derive subtotal: check request payload first; otherwise calculate from user's active cart
        subtotal_raw = request.data.get("subtotal")
        if subtotal_raw is not None:
            try:
                subtotal = Decimal(str(subtotal_raw))
            except Exception:
                subtotal = Decimal("0.00")
        else:
            cart = get_or_create_cart(request)
            subtotal = sum(item.product.current_price * item.quantity for item in cart.items.all())

        discount_amount, error_msg = coupon.calculate_discount(subtotal)
        if error_msg:
            return Response(
                {"detail": error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )

        savings_str = f"{coupon.discount_value}%" if coupon.discount_type == "percentage" else f"${coupon.discount_value:.2f}"
        return Response({
            "valid": True,
            "code": coupon.code,
            "discount_type": coupon.discount_type,
            "discount_value": float(coupon.discount_value),
            "discount_amount": float(discount_amount),
            "message": f"Coupon {coupon.code} applied! Saved ${discount_amount:.2f} ({savings_str} off)."
        })


class CheckoutView(APIView):
    """
    POST /api/orders/checkout/
    Converts the authenticated user's cart into an Order atomically.
    Validates optional coupon, snapshots shipping address and items,
    deducts inventory stock, and clears the cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address_id = serializer.validated_data["address_id"]
        payment_method = serializer.validated_data.get("payment_method", "cod")
        customer_notes = serializer.validated_data.get("customer_notes", "")
        coupon_code = serializer.validated_data.get("coupon_code", "").strip().upper()

        # 1. Fetch address
        address = Address.objects.get(id=address_id, user=request.user)

        # 2. Fetch cart & items
        cart = get_or_create_cart(request)
        cart_items = cart.items.select_related("product").all()

        if not cart_items.exists():
            return Response(
                {"detail": "Your cart is empty. Please add items before placing an order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Check stock availability for every item
        for item in cart_items:
            if item.product.stock_quantity < item.quantity:
                return Response(
                    {
                        "detail": f"Insufficient stock for '{item.product.name}'. Available: {item.product.stock_quantity}, requested: {item.quantity}."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 4. Calculate subtotal & validate coupon if provided
        subtotal = sum(item.product.current_price * item.quantity for item in cart_items)
        shipping_fee = Decimal("0.00")
        discount_amount = Decimal("0.00")
        applied_coupon = None

        if coupon_code:
            applied_coupon = Coupon.objects.filter(code__iexact=coupon_code).first()
            if not applied_coupon:
                return Response(
                    {"detail": f"Coupon code '{coupon_code}' is invalid or expired."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            calc_discount, error_msg = applied_coupon.calculate_discount(subtotal)
            if error_msg:
                return Response(
                    {"detail": f"Cannot apply coupon '{coupon_code}': {error_msg}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            discount_amount = calc_discount

        total_amount = max(Decimal("0.00"), subtotal + shipping_fee - discount_amount)

        # 5. Atomic transaction: create order, create order items, deduct stock, update coupon, clear cart
        with transaction.atomic():
            address_snapshot = {
                "recipient_name": address.recipient_name,
                "phone": address.phone,
                "address_line_1": address.address_line_1,
                "address_line_2": address.address_line_2,
                "city": address.city,
                "state": address.state,
                "postal_code": address.postal_code,
                "country": address.country,
            }

            order = Order.objects.create(
                user=request.user,
                shipping_address_snapshot=address_snapshot,
                subtotal=subtotal,
                shipping_fee=shipping_fee,
                coupon_code=applied_coupon.code if applied_coupon else "",
                discount_amount=discount_amount,
                total_amount=total_amount,
                payment_method=payment_method,
                payment_status="pending",
                order_status="pending",
                customer_notes=customer_notes,
            )

            # Deduct stock and snapshot items
            order_items_to_create = []
            for item in cart_items:
                product = item.product
                product.stock_quantity -= item.quantity
                product.save(update_fields=["stock_quantity"])

                image_url = ""
                if product.image:
                    image_url = request.build_absolute_uri(product.image.url)

                order_items_to_create.append(
                    OrderItem(
                        order=order,
                        product=product,
                        product_name_snapshot=product.name,
                        product_image_snapshot=image_url,
                        unit_price=product.current_price,
                        quantity=item.quantity,
                        line_total=product.current_price * item.quantity,
                    )
                )

            OrderItem.objects.bulk_create(order_items_to_create)

            # Increment coupon usage count
            if applied_coupon:
                Coupon.objects.filter(pk=applied_coupon.pk).update(used_count=F("used_count") + 1)

            # Clear cart
            cart.items.all().delete()

        # Reload order with prefetch for response
        fresh_order = Order.objects.prefetch_related("items__product").get(pk=order.pk)
        return Response(OrderSerializer(fresh_order).data, status=status.HTTP_201_CREATED)


class OrderListView(generics.ListAPIView):
    """
    GET /api/orders/
    Returns list of orders belonging to the logged-in user.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    pagination_class = None

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related("items__product")


class OrderDetailView(APIView):
    """
    GET /api/orders/<order_number>/
    Returns full details for a single order owned by the user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, order_number):
        order = get_object_or_404(
            Order.objects.prefetch_related("items__product"),
            order_number=order_number,
            user=request.user
        )
        return Response(OrderSerializer(order).data)


class PublicOrderTrackView(APIView):
    """
    POST /api/orders/track/
    Payload: { "order_number": "ORD-20261024-XXXX", "email": "customer@example.com" }
    Allows any customer or guest to look up shipment progress and carrier tracking securely.
    """
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        order_number = request.data.get("order_number", "").strip().upper()
        email = request.data.get("email", "").strip().lower()
        if not order_number or not email:
            return Response(
                {"detail": "Please provide both your Order Number and Email address."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order = Order.objects.filter(
            order_number__iexact=order_number,
            user__email__iexact=email
        ).prefetch_related("items").first()
        if not order:
            return Response(
                {"detail": "No order found matching that Order Number and Email address combination."},
                status=status.HTTP_404_NOT_FOUND
            )
        addr = order.shipping_address_snapshot or {}
        items_payload = []
        for it in order.items.all():
            items_payload.append({
                "product_name": it.product_name_snapshot,
                "product_image": it.product_image_snapshot,
                "quantity": it.quantity,
            })
        # Stepper stage index (0 to 3) for the customer UI timeline
        if order.order_status in ["pending", "confirmed"]:
            current_idx = 0
        elif order.order_status == "processing":
            current_idx = 1
        elif order.order_status == "shipped":
            current_idx = 2
        elif order.order_status == "delivered":
            current_idx = 3
        else:
            current_idx = 0
        status_steps = [
            {"key": "pending", "label": "Order Confirmed", "desc": "Order verified in our store system"},
            {"key": "processing", "label": "Sourcing & Packaging", "desc": "Items prepared at dropship warehouse"},
            {"key": "shipped", "label": "In Transit", "desc": "Package handed over to carrier with tracking code"},
            {"key": "delivered", "label": "Delivered", "desc": "Shipment arrived at your destination"}
        ]
        return Response({
            "order_number": order.order_number,
            "order_status": order.order_status,
            "order_status_display": order.get_order_status_display(),
            "tracking_number": order.tracking_number,
            "created_at": order.created_at,
            "updated_at": order.updated_at,
            "recipient_name": addr.get("recipient_name", "Valued Customer"),
            "city": addr.get("city", ""),
            "country": addr.get("country", ""),
            "current_step_index": current_idx,
            "status_steps": status_steps,
            "items": items_payload,
        })
