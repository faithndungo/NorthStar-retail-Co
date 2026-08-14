from rest_framework import viewsets
from .models import Return, ReturnItem
from .serializers import ReturnSerializer, ReturnItemSerializer


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all().order_by('-created_at')
    serializer_class = ReturnSerializer


class ReturnItemViewSet(viewsets.ModelViewSet):
    queryset = ReturnItem.objects.all()
    serializer_class = ReturnItemSerializer

