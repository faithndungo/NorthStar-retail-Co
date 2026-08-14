from django.db import models
from orders.models import Order, OrderItem


class Return(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('received', 'Received'),
        ('refunded', 'Refunded'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='returns'
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='requested'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return #{self.id} for Order #{self.order.id}"


class ReturnItem(models.Model):
    return_request = models.ForeignKey(
        Return,
        on_delete=models.CASCADE,
        related_name='items'
    )

    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.PROTECT,
        related_name='return_items'
    )

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Return Item - Order Item #{self.order_item.id}"
