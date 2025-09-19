from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'email', 'first_name', 'last_name', 'status', 'total_orders',
        'total_spent', 'is_verified', 'created_at'
    ]
    list_filter = ['status', 'is_verified', 'marketing_consent', 'created_at']
    search_fields = ['email', 'first_name', 'last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at', 'total_orders', 'total_spent', 'last_order_date']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'first_name', 'last_name', 'phone')
        }),
        ('Address', {
            'fields': (
                'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country'
            )
        }),
        ('Status & Preferences', {
            'fields': ('status', 'is_verified', 'marketing_consent')
        }),
        ('Statistics', {
            'fields': ('total_orders', 'total_spent', 'last_order_date'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
