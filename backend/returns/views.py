# returns/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from .models import Return, ReturnItem
from .serializers import ReturnSerializer, ReturnItemSerializer


class ReturnEligibilityView(APIView):
    """
    POST /api/returns/eligibility/
    Checks if order is within the 30-day return window.
    """
    def post(self, request):
        order_number = request.data.get('order_number')
        customer_email = request.data.get('customer_email')

        order = Order.objects.filter(
            order_number__iexact=order_number,
            customer_email__iexact=customer_email
        ).first()

        if not order:
            return Response(
                {"error": {"message": "Order not found."}},
                status=status.HTTP_404_NOT_FOUND
            )

        if order.status != 'delivered':
            return Response(
                {"eligible": False, "reason": "Order must be delivered before initiating a return."},
                status=status.HTTP_200_OK
            )

        return_window = timedelta(days=30)
        is_eligible = (timezone.now() - order.created_at) <= return_window

        return Response({
            "eligible": is_eligible,
            "order_number": order.order_number,
            "created_at": order.created_at,
            "reason": "Within 30-day window" if is_eligible else "Return window (30 days) has expired."
        }, status=status.HTTP_200_OK)


class ReturnRequestCreateView(APIView):
    """
    POST /api/returns/requests/
    Creates a return request and generates a dummy shipping label payload.
    """
    def post(self, request):
        order_number = request.data.get('order_number')
        reason = request.data.get('reason', '')
        
        order = Order.objects.filter(order_number__iexact=order_number).first()
        if not order:
            return Response({"error": {"message": "Order not found."}}, status=status.HTTP_404_NOT_FOUND)

        ret = Return.objects.create(order=order, reason=reason, status='requested')

        return Response({
            "message": "Return request created successfully.",
            "return_id": ret.id,
            "shipping_label_url": f"https://shipping-provider.example.com/labels/RET-{ret.id}.pdf"
        }, status=status.HTTP_201_CREATED)


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all().order_by('-created_at')
    serializer_class = ReturnSerializer


class ReturnItemViewSet(viewsets.ModelViewSet):
    queryset = ReturnItem.objects.all()
    serializer_class = ReturnItemSerializer