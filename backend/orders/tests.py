from decimal import Decimal

from rest_framework.test import APITestCase

from accounts.models import CustomerProfile
from inventory.models import Product, ProductVariant
from .models import Order, OrderItem


class OrderLookupTests(APITestCase):
    def setUp(self):
        self.customer = CustomerProfile.objects.create(email='buyer@example.com')
        product = Product.objects.create(name='Jacket', sku='JACKET', price=Decimal('99.00'))
        variant = ProductVariant.objects.create(
            product=product,
            size='M',
            color='Black',
            sku_variant='JACKET-M-BLACK',
            stock_quantity=3,
        )
        self.order = Order.objects.create(customer=self.customer, status='shipped', total_amount=99)
        OrderItem.objects.create(order=self.order, product_variant=variant, quantity=1, unit_price=99)
        self.headers = {'HTTP_X_SESSION_TOKEN': str(self.customer.session_token)}

    def test_lookup_requires_matching_email(self):
        response = self.client.post(
            '/api/orders/lookup/',
            {'order_number': self.order.order_number, 'customer_email': 'wrong@example.com'},
            format='json',
            **self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_lookup_returns_customer_safe_order(self):
        response = self.client.post(
            '/api/orders/lookup/',
            {'order_number': self.order.order_number, 'customer_email': self.customer.email},
            format='json',
            **self.headers,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_number'], self.order.order_number)
        self.assertEqual(len(response.data['items']), 1)
