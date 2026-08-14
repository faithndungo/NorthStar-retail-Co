# accounts/urls.py

from django.urls import path
from .views import SessionTokenView

urlpatterns = [
    path('session/', SessionTokenView.as_view(), name='session-token'),
]