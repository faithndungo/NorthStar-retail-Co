from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.db.models import Sum
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from accounts.session import get_session_profile
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer
from .models import Return, ReturnItem
from .serializers import ReturnSerializer


class OrderIdentitySerializer(serializers.Serializer):
    order_number = serializers.CharField(max_length=24)
    customer_email = serializers.EmailField()


def find_customer_order(data):
    return (
        Order.objects.select_related('customer')
        .prefetch_related('items__product_variant__product')
        .filter(
            order_number__iexact=data['order_number'],
            customer__email__iexact=data['customer_email'],
        )
        .first()
    )


def eligibility_for(order):
    if order.status != 'delivered':
        return False, 'Only delivered orders can be returned.'
    delivered_at = order.delivered_at or order.updated_at
    deadline = delivered_at + timedelta(days=settings.RETURN_WINDOW_DAYS)
    if timezone.now() > deadline:
        return False, f'The {settings.RETURN_WINDOW_DAYS}-day return window has closed.'
    return True, 'This order is eligible for return.'


class ReturnEligibilityView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'order_lookup'

    def post(self, request):
        get_session_profile(request)
        serializer = OrderIdentitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = find_customer_order(serializer.validated_data)
        if order is None:
            return Response(
                {'error': {'message': 'No order matched those details.'}},
                status=status.HTTP_404_NOT_FOUND,
            )
        eligible, message = eligibility_for(order)
        return Response({
            'eligible': eligible,
            'message': message,
            'order': OrderSerializer(order).data if eligible else None,
        })


class ReturnRequestInputSerializer(OrderIdentitySerializer):
    reason = serializers.CharField(max_length=1000)
    item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)


class ReturnRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'return_request'

    @transaction.atomic
    def post(self, request):
        get_session_profile(request)
        serializer = ReturnRequestInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        order = find_customer_order(data)
        if order is None:
            return Response(
                {'error': {'message': 'No order matched those details.'}},
                status=status.HTTP_404_NOT_FOUND,
            )
        eligible, message = eligibility_for(order)
        if not eligible:
            return Response(
                {'error': {'message': message}},
                status=status.HTTP_409_CONFLICT,
            )

        order_item = OrderItem.objects.filter(pk=data['item_id'], order=order).first()
        if order_item is None:
            return Response(
                {'error': {'message': 'The selected item is not part of this order.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        already_returned = (
            ReturnItem.objects.filter(
                order_item=order_item,
                return_request__status__in=['requested', 'approved', 'received', 'refunded'],
            ).aggregate(total=Sum('quantity'))['total'] or 0
        )
        if already_returned + data['quantity'] > order_item.quantity:
            return Response(
                {'error': {'message': 'Return quantity exceeds the remaining eligible quantity.'}},
                status=status.HTTP_409_CONFLICT,
            )

        return_request = Return.objects.create(order=order, reason=data['reason'])
        ReturnItem.objects.create(
            return_request=return_request,
            order_item=order_item,
            quantity=data['quantity'],
        )

        return Response(
            ReturnSerializer(return_request).data,
            status=status.HTTP_201_CREATED,
        )
