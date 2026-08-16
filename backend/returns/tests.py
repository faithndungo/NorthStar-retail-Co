from decimal import Decimal

from django.utils import timezone
from rest_framework.test import APITestCase

from accounts.models import CustomerProfile
from inventory.models import Product, ProductVariant
from orders.models import Order, OrderItem


class ReturnFlowTests(APITestCase):
    def setUp(self):
        self.customer = CustomerProfile.objects.create(email='returns@example.com')
        product = Product.objects.create(name='Shirt', sku='SHIRT', price=Decimal('25.00'))
        variant = ProductVariant.objects.create(
            product=product,
            size='M',
            color='Blue',
            sku_variant='SHIRT-M-BLUE',
            stock_quantity=5,
        )
        self.order = Order.objects.create(
            customer=self.customer,
            status='delivered',
            delivered_at=timezone.now(),
            total_amount=25,
        )
        self.item = OrderItem.objects.create(
            order=self.order,
            product_variant=variant,
            quantity=1,
            unit_price=25,
        )
        self.headers = {'HTTP_X_SESSION_TOKEN': str(self.customer.session_token)}

    def test_eligible_order_can_create_one_return(self):
        identity = {
            'order_number': self.order.order_number,
            'customer_email': self.customer.email,
        }
        eligible = self.client.post(
            '/api/returns/eligibility/', identity, format='json', **self.headers
        )
        self.assertEqual(eligible.status_code, 200)
        self.assertTrue(eligible.data['eligible'])

        payload = {**identity, 'reason': 'wrong_size', 'item_id': self.item.id}
        created = self.client.post(
            '/api/returns/requests/', payload, format='json', **self.headers
        )
        duplicate = self.client.post(
            '/api/returns/requests/', payload, format='json', **self.headers
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(duplicate.status_code, 409)
