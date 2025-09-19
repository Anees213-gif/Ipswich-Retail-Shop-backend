#!/usr/bin/env python
"""
Script to check if sample data exists in the database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')
django.setup()

from apps.core.models import Category
from apps.products.models import Product
from apps.customers.models import Customer
from apps.orders.models import Order

print("=== Database Data Check ===")
print(f"Categories: {Category.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Customers: {Customer.objects.count()}")
print(f"Orders: {Order.objects.count()}")

if Category.objects.count() > 0:
    print("\nCategories:")
    for cat in Category.objects.all()[:5]:
        print(f"  - {cat.name}")

if Product.objects.count() > 0:
    print("\nProducts:")
    for prod in Product.objects.all()[:5]:
        print(f"  - {prod.name} (${prod.price})")

if Customer.objects.count() > 0:
    print("\nCustomers:")
    for cust in Customer.objects.all()[:5]:
        print(f"  - {cust.first_name} {cust.last_name} ({cust.email})")

if Order.objects.count() > 0:
    print("\nOrders:")
    for order in Order.objects.all()[:5]:
        print(f"  - {order.order_number} - ${order.total_amount} ({order.status})")
