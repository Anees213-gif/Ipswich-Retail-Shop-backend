from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_customer_list, name='admin-customer-list'),
    path('<str:email>/', admin_views.AdminCustomerDetailView.as_view(), name='admin-customer-detail'),
    path('stats/', admin_views.customer_stats, name='admin-customer-stats'),
]
