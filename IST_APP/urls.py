from django.urls import path
from . import views
from .views import StockView

app_name = 'IST_APP'

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', StockView.as_view(), name='search'),
    path('results/', views.results, name='results'),
]
