# backend/products/management/commands/seed_products.py
from decimal import Decimal
from django.core.management.base import BaseCommand
from categories.models import Category
from products.models import Product

class Command(BaseCommand):
    help = "Seeds database with realistic dropshipping categories and products"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding categories...")
        cat_tech, _ = Category.objects.get_or_create(
            name="Smart Tech & Gadgets",
            defaults={"description": "Cutting-edge portable tech, wireless audio, and wearables."}
        )
        cat_home, _ = Category.objects.get_or_create(
            name="Home & Lifestyle",
            defaults={"description": "Modern minimalist home aesthetics and smart living tools."}
        )
        cat_fitness, _ = Category.objects.get_or_create(
            name="Fitness & Outdoors",
            defaults={"description": "High-durability fitness gear and outdoor accessories."}
        )

        sample_products = [
            {
                "category": cat_tech,
                "name": "AeroPro Wireless Noise-Cancelling Earbuds",
                "current_price": Decimal("59.99"),
                "original_price": Decimal("89.99"),
                "stock_quantity": 45,
                "rating": Decimal("4.85"),
                "review_count": 128,
                "is_featured": True,
                "description": "Ultra-lightweight wireless earbuds featuring active noise cancellation, 32-hour battery life, and IPX7 water resistance.",
                "specifications": {"Bluetooth": "5.3", "Battery": "32h with case", "Waterproof": "IPX7", "Color": "Matte Black"}
            },
            {
                "category": cat_tech,
                "name": "MagCharge 3-in-1 Foldable Wireless Station",
                "current_price": Decimal("42.50"),
                "original_price": Decimal("59.00"),
                "stock_quantity": 30,
                "rating": Decimal("4.70"),
                "review_count": 84,
                "is_featured": True,
                "description": "Fast-charging foldable dock for phone, smartwatch, and wireless earbuds. Compact for travel.",
                "specifications": {"Output": "15W Fast Charge", "Input": "USB-C", "Compatibility": "Qi-enabled devices"}
            },
            {
                "category": cat_home,
                "name": "AromaGlow Ultrasonic Ambient Diffuser",
                "current_price": Decimal("34.99"),
                "original_price": Decimal("49.99"),
                "stock_quantity": 60,
                "rating": Decimal("4.92"),
                "review_count": 210,
                "is_featured": True,
                "description": "Minimalist ceramic essential oil diffuser with soothing ambient flame lighting effect and auto shut-off.",
                "specifications": {"Capacity": "300ml", "Run Time": "8-10 Hours", "Light Modes": "Warm Amber / Breathe"}
            },
            {
                "category": cat_fitness,
                "name": "TitanFlex Smart Resistance Band Set",
                "current_price": Decimal("28.00"),
                "original_price": Decimal("39.99"),
                "stock_quantity": 80,
                "rating": Decimal("4.65"),
                "review_count": 42,
                "is_featured": False,
                "description": "5-level heavy-duty resistance band kit with door anchor, handles, and digital workout companion app guide.",
                "specifications": {"Resistance": "10lbs to 150lbs stackable", "Material": "Natural Latex", "Includes": "Bag, Straps, Handles"}
            },
        ]

        for p_data in sample_products:
            p, created = Product.objects.get_or_create(
                name=p_data["name"],
                defaults=p_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created product: {p.name}"))
            else:
                self.stdout.write(f"Product already exists: {p.name}")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
