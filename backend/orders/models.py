# orders/models.py

from django.db import models
from accounts.models import CustomerProfile
from inventory.models import ProductVariant


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    # Human-readable order number (e.g., "NS-1001")
    order_number = models.CharField(max_length=50, unique=True)
    customer_email = models.EmailField()
    customer = models.ForeignKey(
        CustomerProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    carrier = models.CharField(max_length=100, blank=True, null=True)
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    tracking_url = models.URLField(blank=True, null=True)
    estimated_delivery = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} ({self.status})"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.PROTECT,
        related_name='order_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_variant} x {self.quantity}"

    @property
    def title(self):
        return f"{self.product_variant.product.name} ({self.product_variant.size} / {self.product_variant.color})"

    @property
    def sku(self):
        return self.product_variant.sku_variant

    @property
    def subtotal(self):
        return self.quantity * self.unit_price