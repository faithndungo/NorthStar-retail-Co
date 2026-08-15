# inventory/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Product, ProductVariant, StockAlert
from .serializers import ProductSerializer, ProductVariantSerializer, StockAlertSerializer

class ProductCatalogView(APIView):
    """
    GET /api/inventory/products/
    Returns full product list with nested variants for frontend dropdown selectors.
    """
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryCheckView(APIView):
    """
    GET /api/inventory/check/?product_id=&variant=&size=&color=
    Checks stock and returns normalized stock_status and available_count.
    """
    def get(self, request):
        product_id = request.query_params.get('product_id')
        variant_id = request.query_params.get('variant')
        size = request.query_params.get('size')
        color = request.query_params.get('color')

        variant = None
        if variant_id:
            variant = ProductVariant.objects.filter(id=variant_id).first()
        elif product_id and size and color:
            variant = ProductVariant.objects.filter(
                product_id=product_id,
                size__iexact=size,
                color__iexact=color
            ).first()

        if not variant:
            return Response(
                {"error": {"message": "Selected product variant not found."}},
                status=status.HTTP_404_NOT_FOUND
            )

        # Determine normalized stock status
        qty = variant.stock_quantity
        if qty <= 0:
            stock_status = "out_of_stock"
        elif qty <= 3:
            stock_status = "low_stock"
        else:
            stock_status = "in_stock"

        return Response({
            "stock_status": stock_status,
            "available_count": qty,
            "variant_id": variant.id
        }, status=status.HTTP_200_OK)


class StockAlertCreateView(generics.CreateAPIView):
    """
    POST /api/inventory/alerts/
    Captures user email for restock notifications.
    """
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {"message": "You will be notified when this variant is back in stock."},
            status=status.HTTP_201_CREATED
        )