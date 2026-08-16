from decimal import Decimal

from rest_framework.test import APITestCase

from accounts.models import CustomerProfile
from .models import Product, ProductVariant


class InventoryApiTests(APITestCase):
    def setUp(self):
        profile = CustomerProfile.objects.create()
        self.headers = {'HTTP_X_SESSION_TOKEN': str(profile.session_token)}
        product = Product.objects.create(name='Sneaker', sku='SHOE', price=Decimal('70.00'))
        self.variant = ProductVariant.objects.create(
            product=product,
            size='42',
            color='White',
            sku_variant='SHOE-42-WHITE',
            stock_quantity=0,
        )

    def test_checks_variant_and_deduplicates_alerts(self):
        checked = self.client.get(
            f'/api/inventory/check/?variant={self.variant.id}',
            **self.headers,
        )
        self.assertEqual(checked.status_code, 200)
        self.assertEqual(checked.data['stock_status'], 'out_of_stock')

        payload = {'variant': self.variant.id, 'email': 'notify@example.com'}
        first = self.client.post('/api/inventory/alerts/', payload, format='json', **self.headers)
        second = self.client.post('/api/inventory/alerts/', payload, format='json', **self.headers)
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 200)
