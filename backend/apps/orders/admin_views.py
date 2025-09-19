from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from apps.authentication.permissions import IsAdminUser
from .models import Order
from .serializers import OrderSerializer, OrderListSerializer


class AdminOrderListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'customer_email']

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
        
        # Sort functionality
        sort_by = self.request.query_params.get('sortBy', 'createdAt')
        sort_order = self.request.query_params.get('sortOrder', 'desc')
        
        if sort_by == 'total':
            order_field = 'total_amount'
        elif sort_by == 'status':
            order_field = 'status'
        else:
            order_field = 'created_at'
        
        if sort_order == 'asc':
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by(f'-{order_field}')
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        # Pagination
        page_size = int(request.query_params.get('pageSize', 20))
        page = int(request.query_params.get('page', 1))
        
        start = (page - 1) * page_size
        end = start + page_size
        paginated_queryset = queryset[start:end]
        
        serializer = self.get_serializer(paginated_queryset, many=True)
        
        return Response({
            'orders': serializer.data,
            'meta': {
                'page': page,
                'pageSize': page_size,
                'totalItems': queryset.count(),
                'totalPages': (queryset.count() + page_size - 1) // page_size
            }
        })


class AdminOrderDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all().prefetch_related('items__product')
    serializer_class = OrderSerializer
    lookup_field = 'order_number'


class AdminOrderUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_number'
    
    def patch(self, request, *args, **kwargs):
        """Handle PATCH requests for order updates"""
        return self.update(request, *args, **kwargs)
