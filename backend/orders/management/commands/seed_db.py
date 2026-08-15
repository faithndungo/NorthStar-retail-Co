# orders/management/commands/seed_db.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from inventory.models import Product, ProductVariant
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = "Seeds database with test mock products and orders (NS-1001 to NS-1005)."

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")

        # Create Products & Variants
        p1, _ = Product.objects.get_or_create(name="Northstar Jacket", sku="prod-001", price=120.00)
        v1, _ = ProductVariant.objects.get_or_create(product=p1, size="M", color="Black", sku_variant="NS-JKT-001", stock_quantity=2)

        p2, _ = Product.objects.get_or_create(name="Northstar Tee", sku="prod-002", price=35.00)
        v2, _ = ProductVariant.objects.get_or_create(product=p2, size="L", color="White", sku_variant="NS-TEE-014", stock_quantity=12)

        # Seed Orders
        now = timezone.now()
        demo_email = "customer@example.com"

        orders_data = [
            {
                "order_number": "NS-1001", "customer_email": demo_email, "status": "shipped",
                "carrier": "UPS", "tracking_number": "1Z999AA10123456784",
                "tracking_url": "https://www.ups.com/track", "estimated_delivery": now + timedelta(days=3)
            },
            {
                "order_number": "NS-1002", "customer_email": demo_email, "status": "delivered",
                "carrier": "FedEx", "tracking_number": "9405500000000000000000",
                "tracking_url": "https://www.fedex.com/track", "estimated_delivery": now - timedelta(days=2)
            },
            {
                "order_number": "NS-1003", "customer_email": demo_email, "status": "processing",
                "carrier": None, "tracking_number": None, "tracking_url": None, "estimated_delivery": now + timedelta(days=7)
            },
            {
                "order_number": "NS-1004", "customer_email": demo_email, "status": "cancelled",
                "carrier": None, "tracking_number": None, "tracking_url": None, "estimated_delivery": None
            },
        ]

        for o_data in orders_data:
            order, created = Order.objects.get_or_create(
                order_number=o_data["order_number"],
                defaults=o_data
            )
            if created:
                OrderItem.objects.create(order=order, product_variant=v1, quantity=1, unit_price=120.00)
                OrderItem.objects.create(order=order, product_variant=v2, quantity=2, unit_price=35.00)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with test orders!"))