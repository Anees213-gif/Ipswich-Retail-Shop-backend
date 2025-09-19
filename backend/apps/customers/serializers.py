from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    total_orders = serializers.ReadOnlyField()
    total_spent = serializers.ReadOnlyField()
    last_order_date = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name', 'phone',
            'address_line1', 'address_line2', 'city', 'state', 'zip_code', 'country',
            'status', 'is_verified', 'marketing_consent', 'total_orders', 'total_spent',
            'last_order_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CustomerListSerializer(serializers.ModelSerializer):
    total_orders = serializers.ReadOnlyField()
    total_spent = serializers.ReadOnlyField()
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Customer
        fields = [
            'id', 'email', 'first_name', 'last_name', 'full_name', 'phone',
            'status', 'total_orders', 'total_spent', 'created_at'
        ]
