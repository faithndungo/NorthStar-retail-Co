from decimal import Decimal

from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import CustomerProfile
from inventory.models import Product, ProductVariant
from orders.models import Order, OrderItem


class Command(BaseCommand):
    help = 'Create an idempotent customer order and catalog for local demos.'

    def handle(self, *args, **options):
        customer, _ = CustomerProfile.objects.get_or_create(email='demo@northstar.test')
        product, _ = Product.objects.update_or_create(
            sku='NS-JKT-001',
            defaults={
                'name': 'NorthStar Trail Jacket',
                'description': 'A lightweight all-weather jacket.',
                'price': Decimal('129.00'),
            },
        )
        variant, _ = ProductVariant.objects.update_or_create(
            sku_variant='NS-JKT-001-M-BLACK',
            defaults={
                'product': product,
                'size': 'M',
                'color': 'Black',
                'stock_quantity': 0,
            },
        )
        order, _ = Order.objects.update_or_create(
            order_number='NS-10023',
            defaults={
                'customer': customer,
                'status': 'delivered',
                'total_amount': Decimal('129.00'),
                'tracking_carrier': 'NorthStar Express',
                'tracking_url': 'https://example.com/tracking/NS-10023',
                'delivered_at': timezone.now(),
            },
        )
        OrderItem.objects.update_or_create(
            order=order,
            product_variant=variant,
            defaults={'quantity': 1, 'unit_price': Decimal('129.00')},
        )

        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write(f'Order: {order.order_number}')
        self.stdout.write(f'Email: {customer.email}')
