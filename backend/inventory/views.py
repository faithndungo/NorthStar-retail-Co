from django.db import IntegrityError
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.session import get_session_profile
from .models import Product, ProductVariant, StockAlert
from .serializers import ProductSerializer


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        get_session_profile(request)
        products = Product.objects.prefetch_related('variants').all().order_by('name')
        return Response({'products': ProductSerializer(products, many=True).data})


class StockCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        get_session_profile(request)
        params = request.query_params
        variants = ProductVariant.objects.select_related('product')

        variant_id = params.get('variant')
        product_id = params.get('product_id')
        sku = params.get('sku_variant')
        if variant_id:
            variants = variants.filter(pk=variant_id)
        elif sku:
            variants = variants.filter(sku_variant__iexact=sku)
        elif product_id:
            if product_id.isdigit():
                variants = variants.filter(product_id=product_id)
            else:
                variants = variants.filter(product__sku__iexact=product_id)
            variants = variants.filter(
                size__iexact=params.get('size', ''),
                color__iexact=params.get('color', ''),
            )
        else:
            return Response(
                {'error': {'message': 'Provide a variant, product ID, or SKU.'}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        variant = variants.first()
        if variant is None:
            return Response(
                {'error': {'message': 'No matching product variant was found.'}},
                status=status.HTTP_404_NOT_FOUND,
            )

        count = variant.stock_quantity
        stock_status = 'out_of_stock' if count == 0 else 'low_stock' if count <= 5 else 'in_stock'
        return Response({
            'variant_id': variant.id,
            'stock_status': stock_status,
            'available_count': count,
        })


class StockAlertInputSerializer(serializers.Serializer):
    variant = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all())
    email = serializers.EmailField()


class StockAlertView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        get_session_profile(request)
        serializer = StockAlertInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variant = serializer.validated_data['variant']
        email = serializer.validated_data['email'].lower()

        if variant.stock_quantity > 0:
            return Response(
                {'error': {'message': 'This variant is currently in stock.'}},
                status=status.HTTP_409_CONFLICT,
            )

        try:
            alert, created = StockAlert.objects.get_or_create(
                variant=variant,
                email=email,
                notified=False,
            )
        except IntegrityError:
            alert = StockAlert.objects.get(variant=variant, email=email, notified=False)
            created = False

        return Response(
            {
                'id': alert.id,
                'message': 'Restock alert created.' if created else 'You already have an active alert.',
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )
