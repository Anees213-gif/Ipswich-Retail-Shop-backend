from django.urls import path
from . import views

urlpatterns = [
    path('', views.CustomerListView.as_view(), name='customer-list'),
    path('<str:email>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    path('stats/', views.customer_stats, name='customer-stats'),
]
