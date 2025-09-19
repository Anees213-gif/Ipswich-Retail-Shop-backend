from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer


class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'is_verified']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CustomerListSerializer
        return CustomerSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(phone__icontains=search)
            )
        
        return queryset


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'email'


@api_view(['GET'])
def customer_stats(request):
    """
    Get customer statistics for admin panel
    """
    from django.db.models import Count, Avg

    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(status='active').count()
    vip_customers = Customer.objects.filter(status='vip').count()
    
    # Average order value per customer
    avg_order_value = Customer.objects.aggregate(
        avg=Avg('total_spent')
    )['avg'] or 0

    return Response({
        'totalCustomers': total_customers,
        'activeCustomers': active_customers,
        'vipCustomers': vip_customers,
        'avgOrderValue': float(avg_order_value)
    })
