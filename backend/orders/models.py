# backend/orders/models.py
import uuid
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from products.models import Product


def generate_order_number():
    date_str = timezone.now().strftime("%Y%m%d")
    random_str = uuid.uuid4().hex[:6].upper()
    return f"ORD-{date_str}-{random_str}"


class Coupon(models.Model):
    DISCOUNT_TYPE_CHOICES = [
        ("percentage", "Percentage Discount (%)"),
        ("fixed", "Fixed Dollar Discount ($)"),
    ]

    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Coupon code in uppercase (e.g., WELCOME10, SAVE20)"
    )
    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default="percentage"
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Percentage off (e.g. 15 for 15%) or flat dollar amount (e.g. 20.00 for $20 off)"
    )
    min_order_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Minimum subtotal required to apply this coupon"
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Optional ceiling cap for percentage discounts (e.g., max $50 off)"
    )
    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Max times this coupon can be redeemed across the site (leave blank for unlimited)"
    )
    used_count = models.PositiveIntegerField(
        default=0,
        editable=False,
        help_text="Number of completed orders that used this coupon"
    )
    valid_from = models.DateTimeField(default=timezone.now)
    valid_until = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expiration date & time (leave blank for no expiry)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Toggle to immediately disable or enable this coupon"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        type_str = f"{self.discount_value}%" if self.discount_type == "percentage" else f"${self.discount_value}"
        return f"{self.code} ({type_str} off)"

    def clean(self):
        if self.code:
            self.code = self.code.strip().upper()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def calculate_discount(self, subtotal: Decimal):
        """
        Calculates the discount amount based on the provided subtotal.
        Returns a tuple: (discount_amount: Decimal, error_message: str | None)
        """
        if not self.is_active:
            return Decimal("0.00"), "This coupon is no longer active."

        now = timezone.now()
        if self.valid_from and now < self.valid_from:
            return Decimal("0.00"), "This coupon is not active yet."

        if self.valid_until and now > self.valid_until:
            return Decimal("0.00"), "This coupon has expired."

        if self.usage_limit is not None and self.used_count >= self.usage_limit:
            return Decimal("0.00"), "This coupon has reached its maximum usage limit."

        if subtotal < self.min_order_amount:
            return Decimal("0.00"), f"Minimum order subtotal of ${self.min_order_amount:.2f} is required for this coupon."

        if self.discount_type == "percentage":
            discount = (subtotal * self.discount_value) / Decimal("100.00")
            if self.max_discount_amount and discount > self.max_discount_amount:
                discount = self.max_discount_amount
        else:
            # Fixed dollar discount cannot exceed total subtotal
            discount = min(self.discount_value, subtotal)

        return round(discount, 2), None


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("cod", "Cash on Delivery"),
        ("card", "Credit / Debit Card (Sandbox)"),
        ("bank", "Bank Direct Transfer"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("unpaid", "Unpaid"),
        ("pending", "Pending Verification"),
        ("paid", "Paid"),
        ("refunded", "Refunded"),
    ]

    ORDER_STATUS_CHOICES = [
        ("pending", "Order Placed"),
        ("confirmed", "Confirmed"),
        ("processing", "Processing & Sourcing"),
        ("shipped", "Shipped / In Transit"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    order_number = models.CharField(
        max_length=40,
        unique=True,
        default=generate_order_number,
        editable=False,
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    # Address snapshot at the time order was submitted
    shipping_address_snapshot = models.JSONField(
        help_text="Snapshot of the recipient name, phone, and full address at purchase time"
    )

    # Financial breakdown & Applied Coupon
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    coupon_code = models.CharField(max_length=50, blank=True, default="", help_text="Promotional coupon code applied")
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Payment details
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cod"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    # Fulfillment status
    order_status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default="pending"
    )
    tracking_number = models.CharField(max_length=100, blank=True, default="")
    customer_notes = models.TextField(blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_number} - {self.user.username} (${self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items"
    )
    product_name_snapshot = models.CharField(max_length=255)
    product_image_snapshot = models.CharField(max_length=500, blank=True, default="")

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if not self.line_total:
            self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product_name_snapshot} ({self.order.order_number})"
