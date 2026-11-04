# backend/orders/management/commands/seed_coupons.py
from decimal import Decimal
from django.core.management.base import BaseCommand
from orders.models import Coupon


class Command(BaseCommand):
    help = "Seeds initial promotional coupon codes"

    def handle(self, *args, **options):
        coupons_data = [
            {
                "code": "WELCOME10",
                "discount_type": "percentage",
                "discount_value": Decimal("10.00"),
                "min_order_amount": Decimal("0.00"),
                "max_discount_amount": Decimal("25.00"),
                "is_active": True,
            },
            {
                "code": "SAVE20",
                "discount_type": "fixed",
                "discount_value": Decimal("20.00"),
                "min_order_amount": Decimal("50.00"),
                "max_discount_amount": None,
                "is_active": True,
            },
            {
                "code": "FLASH50",
                "discount_type": "percentage",
                "discount_value": Decimal("50.00"),
                "min_order_amount": Decimal("40.00"),
                "max_discount_amount": Decimal("30.00"),
                "is_active": True,
            },
        ]

        created_count = 0
        for item in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=item["code"],
                defaults=item
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created coupon: {coupon.code}"))
            else:
                self.stdout.write(f"Coupon already exists: {coupon.code}")

        self.stdout.write(self.style.SUCCESS(f"Done! {created_count} coupons created."))
