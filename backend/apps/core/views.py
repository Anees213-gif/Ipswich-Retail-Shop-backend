from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
import datetime
import psutil
import os
from .models import Category
from .serializers import CategorySerializer


@api_view(['GET'])
def api_root(request):
    """
    API root endpoint providing information about available endpoints.
    """
    return Response({
        'message': 'Welcome to Ipswich Retail API',
        'version': '1.0.0',
        'status': 'healthy',
        'endpoints': {
            'categories': '/api/categories/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'customers': '/api/customers/',
            'admin': '/admin/',
        }
    })


@api_view(['GET'])
def health_check(request):
    """
    Comprehensive health check endpoint for monitoring and deployment.
    """
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Get system information
    try:
        memory_info = psutil.virtual_memory()
        disk_info = psutil.disk_usage('/')
        system_info = {
            'memory': {
                'total': memory_info.total,
                'available': memory_info.available,
                'percent': memory_info.percent
            },
            'disk': {
                'total': disk_info.total,
                'free': disk_info.free,
                'percent': (disk_info.used / disk_info.total) * 100
            }
        }
    except Exception:
        system_info = None
    
    return Response({
        'status': 'healthy',
        'version': '1.0.0',
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'database': db_status,
        'services': {
            'django': 'running',
            'database': db_status,
        },
        'system': system_info,
        'environment': {
            'debug': settings.DEBUG,
            'allowed_hosts': settings.ALLOWED_HOSTS,
        }
    })


@api_view(['GET'])
def metrics(request):
    """
    Prometheus-style metrics endpoint for monitoring.
    """
    try:
        # Basic application metrics
        from apps.products.models import Product
        from apps.orders.models import Order
        from apps.customers.models import Customer
        
        metrics_data = {
            'application_info{version="1.0.0"}': 1,
            'products_total': Product.objects.count(),
            'products_active': Product.objects.filter(is_active=True).count(),
            'products_featured': Product.objects.filter(is_featured=True).count(),
            'orders_total': Order.objects.count(),
            'customers_total': Customer.objects.count(),
        }
        
        # Add system metrics if available
        try:
            memory_info = psutil.virtual_memory()
            metrics_data.update({
                'system_memory_usage_bytes': memory_info.used,
                'system_memory_total_bytes': memory_info.total,
                'system_memory_usage_percent': memory_info.percent,
            })
        except Exception:
            pass
        
        # Format as Prometheus metrics
        metrics_text = ""
        for metric, value in metrics_data.items():
            metrics_text += f"{metric} {value}\n"
        
        return Response(metrics_text, content_type='text/plain')
        
    except Exception as e:
        return Response({
            'error': 'Failed to collect metrics',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filterset_fields = ['name', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'pk'
