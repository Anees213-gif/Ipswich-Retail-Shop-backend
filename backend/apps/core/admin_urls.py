from django.urls import path
from . import admin_views

urlpatterns = [
    path('dashboard/', admin_views.admin_dashboard, name='admin-dashboard'),
    path('dashboard/stats/', admin_views.dashboard_stats, name='admin-dashboard-stats'),
]
