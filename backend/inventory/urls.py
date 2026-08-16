# inventory/urls.py

from django.urls import path
from .views import ProductListView, StockCheckView, StockAlertView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('check/', StockCheckView.as_view(), name='stock-check'),
    path('alert/', StockAlertView.as_view(), name='stock-alert'),
    path('alerts/', StockAlertView.as_view(), name='stock-alerts'),
]
