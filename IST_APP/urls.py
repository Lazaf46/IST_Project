# IST_APP/urls.py

from django.urls import path
from .views import stock_dashboard, get_stock_data

urlpatterns = [
    path('', stock_dashboard, name='stock_dashboard'),
    path('get_data/', get_stock_data, name='get_stock_data'),  # Ensure the name matches 'stock_data'
]
