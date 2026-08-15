# orders/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Order, OrderItem
from .serializers import OrderDetailSerializer, OrderLookupSerializer, OrderItemSerializer


class OrderLookupView(APIView):
    """
    POST /api/orders/lookup/
    Validates order_number + customer_email and returns shipping status details.
    """
    def post(self, request):
        serializer = OrderLookupSerializer(data=request.data)
        if serializer.is_valid():
            order_number = serializer.validated_data['order_number']
            customer_email = serializer.validated_data['customer_email']

            order = Order.objects.filter(
                order_number__iexact=order_number,
                customer_email__iexact=customer_email
            ).first()

            if not order:
                return Response(
                    {"error": {"message": "No order found matching the provided order number and email."}},
                    status=status.HTTP_404_NOT_FOUND
                )

            return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailByNumberView(APIView):
    """
    GET /api/orders/{order_number}/
    """
    def get(self, request, order_number):
        order = Order.objects.filter(order_number__iexact=order_number).first()
        if not order:
            return Response(
                {"error": {"message": f"Order {order_number} not found."}},
                status=status.HTTP_404_NOT_FOUND
            )
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderDetailSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer