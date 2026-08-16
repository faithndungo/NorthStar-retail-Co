from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from accounts.session import get_session_profile
from .models import Order
from .serializers import OrderSerializer


class OrderLookupInputSerializer(serializers.Serializer):
    order_number = serializers.CharField(max_length=24)
    customer_email = serializers.EmailField()


class OrderLookupView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'order_lookup'

    def post(self, request):
        get_session_profile(request)
        serializer = OrderLookupInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = (
            Order.objects.select_related('customer')
            .prefetch_related('items__product_variant__product')
            .filter(
                order_number__iexact=serializer.validated_data['order_number'],
                customer__email__iexact=serializer.validated_data['customer_email'],
            )
            .first()
        )
        if order is None:
            return Response(
                {'error': {'message': 'No order matched those details.'}},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(OrderSerializer(order).data)
