# inventory/urls.py

from django.urls import path
from .views import ProductCatalogView, InventoryCheckView, StockAlertCreateView

urlpatterns = [
    path('products/', ProductCatalogView.as_view(), name='product-catalog'),
    path('check/', InventoryCheckView.as_view(), name='inventory-check'),
    path('alerts/', StockAlertCreateView.as_view(), name='stock-alerts'),  # Note: plural 'alerts/'
]