# inventory/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Product, ProductVariant, StockAlert
from .serializers import ProductSerializer, ProductVariantSerializer, StockAlertSerializer

class StockCheckView(APIView):
    """
    GET /api/inventory/check/
    Optionally filter by ?sku_variant=<sku> or return all products with stock info.
    """
    def get(self, request):
        sku_variant = request.query_params.get('sku_variant')
        if sku_variant:
            try:
                variant = ProductVariant.objects.get(sku_variant=sku_variant)
                serializer = ProductVariantSerializer(variant)
                return Response({"data": serializer.data}, status=status.HTTP_200_OK)
            except ProductVariant.DoesNotExist:
                return Response(
                    {"error": f"Variant with SKU '{sku_variant}' not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class StockAlertView(generics.CreateAPIView):
    """
    POST /api/inventory/alert/
    Registers a restock notification alert for out-of-stock items.
    """
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer