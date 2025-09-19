from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from apps.authentication.permissions import IsAdminUser
from apps.orders.models import Order
from apps.products.models import Product
from apps.customers.models import Customer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_dashboard(request):
    """
    Admin dashboard overview - returns actual dashboard stats
    """
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)

    # Orders today
    orders_today = Order.objects.filter(created_at__date=today).count()
    
    # Revenue today
    revenue_today = Order.objects.filter(
        created_at__date=today,
        status__in=['completed', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Orders this week
    orders_week = Order.objects.filter(created_at__date__gte=week_ago).count()
    
    # Revenue this week
    revenue_week = Order.objects.filter(
        created_at__date__gte=week_ago,
        status__in=['completed', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Total products
    total_products = Product.objects.count()
    
    # Total customers
    total_customers = Customer.objects.count()
    
    # Total orders
    total_orders = Order.objects.count()
    
    # Total revenue
    total_revenue = Order.objects.filter(
        status__in=['completed', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0

    # Calculate average order value
    avg_order_value = 0
    if total_orders > 0:
        avg_order_value = float(total_revenue) / total_orders
    
    # Calculate orders for last 7 days
    orders_last_7_days = []
    for i in range(7):
        date = today - timedelta(days=i)
        orders_count = Order.objects.filter(created_at__date=date).count()
        orders_last_7_days.append({
            'date': date.strftime('%Y-%m-%d'),
            'orders': orders_count
        })
    orders_last_7_days.reverse()  # Show oldest to newest
    
    # Calculate error rate (cancelled orders / total orders)
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    error_rate = (cancelled_orders / total_orders * 100) if total_orders > 0 else 0

    return Response({
        'ordersToday': orders_today,
        'revenueToday': float(revenue_today),
        'avgOrderValue': avg_order_value,
        'errorRate': error_rate,
        'ordersLast7Days': orders_last_7_days,
    })


@api_view(['GET'])
@permission_classes([IsAdminUser])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin panel
    """
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)

    # Orders today
    orders_today = Order.objects.filter(created_at__date=today).count()
    
    # Revenue today
    revenue_today = Order.objects.filter(
        created_at__date=today,
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Average order value
    avg_order_value = Order.objects.filter(
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(avg=Avg('total_amount'))['avg'] or 0
    
    # Orders last 7 days
    orders_last_7_days = []
    for i in range(7):
        date = today - timedelta(days=i)
        count = Order.objects.filter(created_at__date=date).count()
        orders_last_7_days.append({
            'date': date.isoformat(),
            'orders': count
        })
    
    # Error rate (cancelled orders)
    total_orders = Order.objects.count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()
    error_rate = (cancelled_orders / total_orders * 100) if total_orders > 0 else 0

    return Response({
        'ordersToday': orders_today,
        'revenueToday': float(revenue_today),
        'avgOrderValue': float(avg_order_value),
        'errorRate': round(error_rate, 1),
        'ordersLast7Days': list(reversed(orders_last_7_days))
    })
