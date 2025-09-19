from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q, Count, Avg
from apps.authentication.permissions import IsAdminUser
from .models import Customer
from .serializers import CustomerSerializer, CustomerListSerializer


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_customer_list(request):
    """
    List all customers for admin panel
    """
    queryset = Customer.objects.all()
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    # Status filter
    status = request.GET.get('status')
    if status:
        queryset = queryset.filter(status=status)
    
    # Pagination
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('pageSize', 20))
    start = (page - 1) * page_size
    end = start + page_size
    
    paginated_queryset = queryset[start:end]
    serializer = CustomerListSerializer(paginated_queryset, many=True)
    
    return Response({
        'customers': serializer.data,
        'meta': {
            'page': page,
            'pageSize': page_size,
            'totalItems': queryset.count(),
            'totalPages': (queryset.count() + page_size - 1) // page_size,
            'hasNext': end < queryset.count(),
            'hasPrevious': page > 1,
        }
    })


class AdminCustomerDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser]
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'email'


@api_view(['GET'])
@permission_classes([IsAdminUser])
def customer_stats(request):
    """
    Get customer statistics for admin panel
    """
    total_customers = Customer.objects.count()
    active_customers = Customer.objects.filter(status='active').count()
    vip_customers = Customer.objects.filter(status='vip').count()
    
    # Calculate average order value per customer
    customers = Customer.objects.all()
    total_spent = sum(customer.total_spent for customer in customers)
    avg_order_value = total_spent / total_customers if total_customers > 0 else 0

    return Response({
        'totalCustomers': total_customers,
        'activeCustomers': active_customers,
        'vipCustomers': vip_customers,
        'avgOrderValue': float(avg_order_value)
    })
