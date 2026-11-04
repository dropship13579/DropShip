# backend/products/management/commands/seed_suppliers.py
from decimal import Decimal
from django.core.management.base import BaseCommand
from products.models import Supplier, Product


class Command(BaseCommand):
    help = "Seeds initial dropship suppliers and connects existing products with supplier wholesale costs"

    def handle(self, *args, **options):
        suppliers_data = [
            {
                "name": "CJ Dropshipping",
                "contact_name": "Andy CJ Rep",
                "email": "support@cjdropshipping.com",
                "website_url": "https://cjdropshipping.com",
                "average_shipping_days": 8,
                "notes": "Direct factory partner with CJ Express line.",
                "is_active": True,
            },
            {
                "name": "AliExpress Direct",
                "contact_name": "Shenzhen Logistics Hub",
                "email": "vendor@aliexpress.com",
                "website_url": "https://aliexpress.com",
                "average_shipping_days": 12,
                "notes": "ePacket tracking with Cainiao Global dispatch.",
                "is_active": True,
            },
            {
                "name": "Spocket Global",
                "contact_name": "EU/US Warehouses",
                "email": "dispatch@spocket.co",
                "website_url": "https://spocket.co",
                "average_shipping_days": 4,
                "notes": "Fast domestic fulfillment inside US and Europe.",
                "is_active": True,
            },
        ]

        suppliers_map = {}
        for s_data in suppliers_data:
            sup, _ = Supplier.objects.get_or_create(name=s_data["name"], defaults=s_data)
            suppliers_map[sup.name] = sup
            self.stdout.write(self.style.SUCCESS(f"Supplier ready: {sup.name}"))

        # Connect existing demo products with wholesale supplier costs
        cj = suppliers_map.get("CJ Dropshipping")
        ali = suppliers_map.get("AliExpress Direct")
        spocket = suppliers_map.get("Spocket Global")

        products = Product.objects.all()
        for idx, p in enumerate(products):
            # Assign supplier and a realistic ~40-60% margin wholesale cost
            if idx % 3 == 0:
                p.supplier = spocket
                p.supplier_cost = round(Decimal(str(p.current_price)) * Decimal("0.45"), 2)
                p.supplier_sku = f"SPK-{p.id:04d}"
            elif idx % 3 == 1:
                p.supplier = cj
                p.supplier_cost = round(Decimal(str(p.current_price)) * Decimal("0.38"), 2)
                p.supplier_sku = f"CJ-{p.id:04d}"
            else:
                p.supplier = ali
                p.supplier_cost = round(Decimal(str(p.current_price)) * Decimal("0.32"), 2)
                p.supplier_sku = f"ALI-{p.id:04d}"

            p.save(update_fields=["supplier", "supplier_cost", "supplier_sku"])
            self.stdout.write(f"Updated product: {p.name} (Cost: ${p.supplier_cost}, Margin: {p.profit_margin_percentage}%)")

        self.stdout.write(self.style.SUCCESS("Done! All suppliers seeded and product costs computed."))
