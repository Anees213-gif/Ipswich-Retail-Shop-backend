#!/usr/bin/env python
"""
Script to create comprehensive sample data for the e-commerce application
"""
import os
import sys
import django
from decimal import Decimal
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Category
from apps.products.models import Product, ProductImage, ProductSpecification, ProductTag
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem

def create_categories():
    """Create product categories"""
    categories_data = [
        {'name': 'Electronics', 'description': 'Latest tech gadgets and devices', 'slug': 'electronics'},
        {'name': 'Apparel', 'description': 'Fashion and clothing for all', 'slug': 'apparel'},
        {'name': 'Home & Garden', 'description': 'Everything for your home and garden', 'slug': 'home-garden'},
        {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear', 'slug': 'sports-outdoors'},
        {'name': 'Books & Media', 'description': 'Books, movies, and digital media', 'slug': 'books-media'},
        {'name': 'Beauty & Health', 'description': 'Beauty products and health supplements', 'slug': 'beauty-health'},
        {'name': 'Toys & Games', 'description': 'Fun toys and games for all ages', 'slug': 'toys-games'},
        {'name': 'Automotive', 'description': 'Car accessories and automotive parts', 'slug': 'automotive'},
    ]
    
    categories = {}
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': cat_data['slug']
            }
        )
        categories[cat_data['name']] = category
        if created:
            print(f'✅ Created category: {category.name}')
        else:
            print(f'📁 Category already exists: {category.name}')
    
    return categories

def create_products(categories):
    """Create sample products"""
    products_data = [
        # Electronics
        {
            'name': 'Premium Wireless Headphones',
            'slug': 'premium-wireless-headphones',
            'description': 'High-quality wireless headphones with noise cancellation and premium sound quality. Perfect for music lovers and professionals.',
            'price': Decimal('299.99'),
            'original_price': Decimal('399.99'),
            'category': 'Electronics',
            'stock_count': 25,
            'is_featured': True,
            'rating': 4.8,
            'review_count': 156,
            'specifications': {
                'Battery Life': '30 hours',
                'Driver Size': '40mm',
                'Frequency Response': '20Hz - 20kHz',
                'Weight': '250g',
                'Connectivity': 'Bluetooth 5.0',
                'Noise Cancellation': 'Active'
            },
            'tags': ['wireless', 'noise-cancelling', 'premium', 'bluetooth']
        },
        {
            'name': 'Smart Fitness Watch',
            'slug': 'smart-fitness-watch',
            'description': 'Advanced fitness tracking with heart rate monitoring, GPS, and 7-day battery life.',
            'price': Decimal('199.99'),
            'original_price': Decimal('249.99'),
            'category': 'Electronics',
            'stock_count': 40,
            'is_featured': True,
            'rating': 4.6,
            'review_count': 89,
            'specifications': {
                'Battery Life': '7 days',
                'Water Resistance': '5ATM',
                'Display': '1.4" AMOLED',
                'Sensors': 'Heart Rate, GPS, Accelerometer',
                'Compatibility': 'iOS, Android'
            },
            'tags': ['fitness', 'smartwatch', 'health', 'gps']
        },
        {
            'name': '4K Ultra HD TV 55"',
            'slug': '4k-ultra-hd-tv-55',
            'description': 'Stunning 4K picture quality with HDR support and smart TV features.',
            'price': Decimal('899.99'),
            'original_price': Decimal('1199.99'),
            'category': 'Electronics',
            'stock_count': 15,
            'is_featured': True,
            'rating': 4.7,
            'review_count': 234,
            'specifications': {
                'Screen Size': '55 inches',
                'Resolution': '4K Ultra HD (3840x2160)',
                'HDR': 'HDR10, Dolby Vision',
                'Smart TV': 'Built-in',
                'Connectivity': 'WiFi, Bluetooth, 4 HDMI'
            },
            'tags': ['4k', 'smart-tv', 'hdr', 'entertainment']
        },
        
        # Apparel
        {
            'name': 'Organic Cotton T-Shirt',
            'slug': 'organic-cotton-t-shirt',
            'description': 'Comfortable organic cotton t-shirt in various colors. Sustainably sourced and ethically made.',
            'price': Decimal('39.99'),
            'category': 'Apparel',
            'stock_count': 50,
            'is_featured': True,
            'rating': 4.5,
            'review_count': 89,
            'specifications': {
                'Material': '100% Organic Cotton',
                'Fit': 'Regular',
                'Care': 'Machine wash cold',
                'Origin': 'Fair Trade Certified'
            },
            'tags': ['organic', 'sustainable', 'casual', 'cotton']
        },
        {
            'name': 'Premium Denim Jeans',
            'slug': 'premium-denim-jeans',
            'description': 'Classic fit denim jeans made from premium cotton with a comfortable stretch.',
            'price': Decimal('89.99'),
            'original_price': Decimal('120.00'),
            'category': 'Apparel',
            'stock_count': 30,
            'is_featured': False,
            'rating': 4.3,
            'review_count': 67,
            'specifications': {
                'Material': '98% Cotton, 2% Elastane',
                'Fit': 'Classic',
                'Rise': 'Mid-rise',
                'Care': 'Machine wash cold'
            },
            'tags': ['denim', 'jeans', 'classic', 'comfortable']
        },
        
        # Home & Garden
        {
            'name': 'Smart Home Security Camera',
            'slug': 'smart-home-security-camera',
            'description': 'Wireless security camera with night vision, motion detection, and mobile app control.',
            'price': Decimal('149.99'),
            'original_price': Decimal('199.99'),
            'category': 'Home & Garden',
            'stock_count': 20,
            'is_featured': True,
            'rating': 4.4,
            'review_count': 123,
            'specifications': {
                'Resolution': '1080p HD',
                'Night Vision': '30ft range',
                'Storage': 'Cloud & Local',
                'Connectivity': 'WiFi',
                'Power': 'Battery & Solar'
            },
            'tags': ['security', 'smart-home', 'camera', 'wireless']
        },
        {
            'name': 'Indoor Plant Collection',
            'slug': 'indoor-plant-collection',
            'description': 'Beautiful collection of easy-care indoor plants perfect for home decoration.',
            'price': Decimal('79.99'),
            'category': 'Home & Garden',
            'stock_count': 35,
            'is_featured': False,
            'rating': 4.6,
            'review_count': 45,
            'specifications': {
                'Plants Included': '5 different varieties',
                'Pot Material': 'Ceramic',
                'Care Level': 'Easy',
                'Light Requirements': 'Bright indirect'
            },
            'tags': ['plants', 'indoor', 'decorative', 'easy-care']
        },
        
        # Sports & Outdoors
        {
            'name': 'Professional Yoga Mat',
            'slug': 'professional-yoga-mat',
            'description': 'Non-slip yoga mat with excellent grip and cushioning for all yoga practices.',
            'price': Decimal('59.99'),
            'original_price': Decimal('79.99'),
            'category': 'Sports & Outdoors',
            'stock_count': 60,
            'is_featured': True,
            'rating': 4.7,
            'review_count': 178,
            'specifications': {
                'Material': 'TPE (Thermoplastic Elastomer)',
                'Thickness': '6mm',
                'Size': '72" x 24"',
                'Weight': '2.5 lbs',
                'Grip': 'Non-slip surface'
            },
            'tags': ['yoga', 'fitness', 'non-slip', 'professional']
        },
        {
            'name': 'Camping Tent 4-Person',
            'slug': 'camping-tent-4-person',
            'description': 'Spacious 4-person tent with weather protection and easy setup.',
            'price': Decimal('199.99'),
            'original_price': Decimal('279.99'),
            'category': 'Sports & Outdoors',
            'stock_count': 12,
            'is_featured': False,
            'rating': 4.5,
            'review_count': 92,
            'specifications': {
                'Capacity': '4 people',
                'Weight': '8.5 lbs',
                'Setup Time': '10 minutes',
                'Weather Protection': 'Waterproof',
                'Ventilation': 'Mesh panels'
            },
            'tags': ['camping', 'tent', 'outdoor', 'waterproof']
        },
        
        # Books & Media
        {
            'name': 'Programming Fundamentals Book',
            'slug': 'programming-fundamentals-book',
            'description': 'Comprehensive guide to programming fundamentals with practical examples.',
            'price': Decimal('49.99'),
            'category': 'Books & Media',
            'stock_count': 80,
            'is_featured': True,
            'rating': 4.8,
            'review_count': 156,
            'specifications': {
                'Pages': '450',
                'Format': 'Paperback',
                'Language': 'English',
                'Publisher': 'Tech Books Inc',
                'Edition': '3rd Edition'
            },
            'tags': ['programming', 'education', 'book', 'fundamentals']
        },
        
        # Beauty & Health
        {
            'name': 'Organic Skincare Set',
            'slug': 'organic-skincare-set',
            'description': 'Complete organic skincare routine with cleanser, toner, and moisturizer.',
            'price': Decimal('89.99'),
            'original_price': Decimal('120.00'),
            'category': 'Beauty & Health',
            'stock_count': 25,
            'is_featured': True,
            'rating': 4.6,
            'review_count': 134,
            'specifications': {
                'Products': '3-piece set',
                'Skin Type': 'All skin types',
                'Ingredients': '100% Organic',
                'Cruelty Free': 'Yes',
                'Size': 'Full size products'
            },
            'tags': ['skincare', 'organic', 'beauty', 'cruelty-free']
        },
        
        # Toys & Games
        {
            'name': 'Educational Building Blocks Set',
            'slug': 'educational-building-blocks-set',
            'description': 'Creative building blocks set that promotes learning and creativity.',
            'price': Decimal('79.99'),
            'category': 'Toys & Games',
            'stock_count': 40,
            'is_featured': False,
            'rating': 4.7,
            'review_count': 89,
            'specifications': {
                'Pieces': '200+ blocks',
                'Age Range': '3-8 years',
                'Material': 'Safe plastic',
                'Educational Value': 'STEM learning',
                'Storage': 'Included container'
            },
            'tags': ['toys', 'educational', 'building', 'kids']
        },
        
        # Automotive
        {
            'name': 'Car Phone Mount',
            'slug': 'car-phone-mount',
            'description': 'Secure phone mount for car dashboard with 360-degree rotation.',
            'price': Decimal('29.99'),
            'original_price': Decimal('39.99'),
            'category': 'Automotive',
            'stock_count': 100,
            'is_featured': False,
            'rating': 4.4,
            'review_count': 267,
            'specifications': {
                'Mount Type': 'Dashboard',
                'Rotation': '360 degrees',
                'Compatibility': 'Universal',
                'Material': 'ABS plastic',
                'Installation': 'No tools required'
            },
            'tags': ['car', 'phone-mount', 'automotive', 'universal']
        }
    ]
    
    for product_data in products_data:
        category = categories[product_data['category']]
        
        # Create or get product
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults={
                'slug': product_data['slug'],
                'description': product_data['description'],
                'price': product_data['price'],
                'original_price': product_data.get('original_price'),
                'category': category,
                'stock_count': product_data['stock_count'],
                'is_featured': product_data['is_featured'],
                'rating': product_data['rating'],
                'review_count': product_data['review_count'],
            }
        )
        
        if created:
            print(f'✅ Created product: {product.name}')
            
            # Add specifications
            for key, value in product_data['specifications'].items():
                ProductSpecification.objects.create(
                    product=product,
                    name=key,
                    value=value
                )
            
            # Add tags
            for tag_name in product_data['tags']:
                tag, _ = ProductTag.objects.get_or_create(name=tag_name)
                product.tags.add(tag)
            
            # Add placeholder images
            for i in range(2):
                ProductImage.objects.create(
                    product=product,
                    image=f'/api/placeholder/400/400',
                    alt_text=f'{product.name} - Image {i+1}'
                )
        else:
            print(f'📦 Product already exists: {product.name}')

def create_customers():
    """Create sample customers"""
    customers_data = [
        {
            'email': 'john.doe@email.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '+1-555-0123',
            'status': 'active',
            'address_line1': '123 Main St',
            'city': 'New York',
            'state': 'NY',
            'zip_code': '10001',
            'is_verified': True
        },
        {
            'email': 'jane.smith@email.com',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'phone': '+1-555-0124',
            'status': 'vip',
            'address_line1': '456 Oak Ave',
            'city': 'Los Angeles',
            'state': 'CA',
            'zip_code': '90210',
            'is_verified': True
        },
        {
            'email': 'mike.johnson@email.com',
            'first_name': 'Mike',
            'last_name': 'Johnson',
            'phone': '+1-555-0125',
            'status': 'active',
            'address_line1': '789 Pine Rd',
            'city': 'Chicago',
            'state': 'IL',
            'zip_code': '60601',
            'is_verified': True
        },
        {
            'email': 'sarah.wilson@email.com',
            'first_name': 'Sarah',
            'last_name': 'Wilson',
            'phone': '+1-555-0126',
            'status': 'active',
            'address_line1': '321 Elm St',
            'city': 'Houston',
            'state': 'TX',
            'zip_code': '77001',
            'is_verified': True
        },
        {
            'email': 'david.brown@email.com',
            'first_name': 'David',
            'last_name': 'Brown',
            'phone': '+1-555-0127',
            'status': 'inactive',
            'address_line1': '654 Maple Dr',
            'city': 'Phoenix',
            'state': 'AZ',
            'zip_code': '85001',
            'is_verified': False
        }
    ]
    
    for customer_data in customers_data:
        customer, created = Customer.objects.get_or_create(
            email=customer_data['email'],
            defaults={
                'first_name': customer_data['first_name'],
                'last_name': customer_data['last_name'],
                'phone': customer_data['phone'],
                'status': customer_data['status'],
                'address_line1': customer_data['address_line1'],
                'city': customer_data['city'],
                'state': customer_data['state'],
                'zip_code': customer_data['zip_code'],
                'is_verified': customer_data['is_verified'],
            }
        )
        if created:
            print(f'✅ Created customer: {customer.first_name} {customer.last_name}')
        else:
            print(f'👤 Customer already exists: {customer.first_name} {customer.last_name}')

def create_orders():
    """Create sample orders"""
    customers = Customer.objects.all()
    products = Product.objects.all()
    
    if not customers.exists() or not products.exists():
        print('⚠️ No customers or products found. Please create them first.')
        return
    
    order_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    for i in range(15):
        customer = random.choice(customers)
        status = random.choice(order_statuses)
        
        # Calculate order totals
        num_items = random.randint(1, 4)
        selected_products = random.sample(list(products), min(num_items, len(products)))
        subtotal = Decimal('0.00')
        
        # Calculate subtotal first
        for product in selected_products:
            quantity = random.randint(1, 3)
            item_total = product.price * quantity
            subtotal += item_total
        
        # Calculate shipping and tax
        shipping_cost = Decimal('9.99') if subtotal < Decimal('50.00') else Decimal('0.00')
        tax_amount = subtotal * Decimal('0.08')  # 8% tax
        total_amount = subtotal + shipping_cost + tax_amount
        
        # Create order
        order = Order.objects.create(
            order_number=f'ORD-{1000 + i}',
            customer_email=customer.email,
            customer_first_name=customer.first_name,
            customer_last_name=customer.last_name,
            customer_phone=customer.phone,
            shipping_address_line1=customer.address_line1,
            shipping_city=customer.city,
            shipping_state=customer.state,
            shipping_zip_code=customer.zip_code,
            subtotal=subtotal,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            total_amount=total_amount,
            status=status,
            created_at=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        
        # Add order items
        for product in selected_products:
            quantity = random.randint(1, 3)
            unit_price = product.price
            
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                total_price=unit_price * quantity
            )
        
        print(f'✅ Created order: {order.order_number} - ${order.total_amount}')

def main():
    """Main function to create all sample data"""
    print('🚀 Creating comprehensive sample data...')
    print('=' * 50)
    
    # Create categories
    print('\n📁 Creating categories...')
    categories = create_categories()
    
    # Create products
    print('\n📦 Creating products...')
    create_products(categories)
    
    # Create customers
    print('\n👤 Creating customers...')
    create_customers()
    
    # Create orders
    print('\n📋 Creating orders...')
    create_orders()
    
    print('\n' + '=' * 50)
    print('✅ Sample data creation completed!')
    print(f'📊 Summary:')
    print(f'   - Categories: {Category.objects.count()}')
    print(f'   - Products: {Product.objects.count()}')
    print(f'   - Customers: {Customer.objects.count()}')
    print(f'   - Orders: {Order.objects.count()}')
    print(f'   - Order Items: {OrderItem.objects.count()}')

if __name__ == '__main__':
    main()
