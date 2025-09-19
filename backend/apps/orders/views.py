from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer


class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer_email']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(customer_email__icontains=search) |
                Q(customer_first_name__icontains=search) |
                Q(customer_last_name__icontains=search)
            )
        
        return queryset


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer
    lookup_field = 'order_number'


@api_view(['GET'])
def dashboard_stats(request):
    """
    Get dashboard statistics for admin panel
    """
    from django.db.models import Count, Sum
    from django.utils import timezone
    from datetime import timedelta

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
    ).aggregate(avg=Sum('total_amount') / Count('id'))['avg'] or 0
    
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
