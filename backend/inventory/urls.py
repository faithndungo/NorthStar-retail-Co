# inventory/urls.py

from django.urls import path
from .views import StockCheckView, StockAlertView

urlpatterns = [
    path('check/', StockCheckView.as_view(), name='stock-check'),
    path('alert/', StockAlertView.as_view(), name='stock-alert'),
]