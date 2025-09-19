from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.AdminOrderListView.as_view(), name='admin-order-list'),
    path('<str:order_number>/', admin_views.AdminOrderDetailView.as_view(), name='admin-order-detail'),
    path('<str:order_number>/update/', admin_views.AdminOrderUpdateView.as_view(), name='admin-order-update'),
]
