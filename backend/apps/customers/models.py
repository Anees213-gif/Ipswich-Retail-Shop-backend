from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('vip', 'VIP'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)
    
    # Address information
    address_line1 = models.CharField(max_length=200, blank=True)
    address_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='US')
    
    # Customer status and preferences
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_verified = models.BooleanField(default=False)
    marketing_consent = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def total_orders(self):
        from apps.orders.models import Order
        return Order.objects.filter(customer_email=self.email).count()

    @property
    def total_spent(self):
        from apps.orders.models import Order
        from django.db.models import Sum
        total = Order.objects.filter(
            customer_email=self.email,
            status__in=['confirmed', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total']
        return total or 0

    @property
    def last_order_date(self):
        from apps.orders.models import Order
        last_order = Order.objects.filter(customer_email=self.email).order_by('-created_at').first()
        return last_order.created_at if last_order else None
