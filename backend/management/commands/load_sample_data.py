from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import Category
from apps.products.models import Product, ProductImage, ProductSpecification, ProductTag
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem
from decimal import Decimal
import os


class Command(BaseCommand):
    help = 'Load sample data for development'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ipswichretail.com',
                password='admin123'
            )
            self.stdout.write('Created admin user: admin@ipswichretail.com / admin123')
        else:
            self.stdout.write('Admin user already exists')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest tech gadgets and devices'},
            {'name': 'Apparel', 'description': 'Fashion and clothing for all'},
            {'name': 'Books', 'description': 'Knowledge and entertainment'},
            {'name': 'Accessories', 'description': 'Complete your style'},
            {'name': 'Home & Garden', 'description': 'Make your space beautiful'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Check if products already exist
        if Product.objects.exists():
            self.stdout.write('Sample data already loaded, skipping...')
            return

        # Create products
        products_data = [
            {
                'name': 'Premium Wireless Headphones',
                'description': 'High-quality wireless headphones with noise cancellation and premium sound quality.',
                'price': Decimal('299.99'),
                'original_price': Decimal('399.99'),
                'category': 'Electronics',
                'stock_count': 25,
                'is_featured': True,
                'rating': Decimal('4.8'),
                'review_count': 156,
                'specifications': {
                    'Battery Life': '30 hours',
                    'Driver Size': '40mm',
                    'Frequency Response': '20Hz - 20kHz',
                    'Weight': '250g'
                },
                'tags': ['wireless', 'noise-cancelling', 'premium']
            },
            {
                'name': 'Organic Cotton T-Shirt',
                'description': 'Comfortable organic cotton t-shirt in various colors. Sustainably sourced and ethically made.',
                'price': Decimal('39.99'),
                'category': 'Apparel',
                'stock_count': 50,
                'is_featured': True,
                'rating': Decimal('4.5'),
                'review_count': 89,
                'specifications': {
                    'Material': '100% Organic Cotton',
                    'Fit': 'Regular',
                    'Care': 'Machine wash cold'
                },
                'tags': ['organic', 'sustainable', 'casual']
            },
            {
                'name': 'JavaScript: The Definitive Guide',
                'description': 'The comprehensive guide to JavaScript programming. Perfect for developers of all levels.',
                'price': Decimal('59.99'),
                'category': 'Books',
                'stock_count': 15,
                'is_featured': True,
                'rating': Decimal('4.7'),
                'review_count': 234,
                'specifications': {
                    'Pages': '1,096',
                    'Publisher': 'O\'Reilly Media',
                    'Edition': '7th',
                    'Language': 'English'
                },
                'tags': ['programming', 'javascript', 'technical']
            },
            {
                'name': 'Smart Fitness Watch',
                'description': 'Advanced fitness tracking with heart rate monitoring, GPS, and long battery life.',
                'price': Decimal('199.99'),
                'original_price': Decimal('249.99'),
                'category': 'Electronics',
                'stock_count': 30,
                'is_featured': False,
                'rating': Decimal('4.6'),
                'review_count': 178,
                'specifications': {
                    'Battery Life': '7 days',
                    'Display': '1.4" AMOLED',
                    'Water Resistance': '5ATM',
                    'Connectivity': 'Bluetooth 5.0, WiFi'
                },
                'tags': ['fitness', 'smartwatch', 'health']
            },
            {
                'name': 'Minimalist Leather Wallet',
                'description': 'Sleek minimalist wallet crafted from premium leather. Holds up to 8 cards.',
                'price': Decimal('79.99'),
                'category': 'Accessories',
                'stock_count': 20,
                'is_featured': False,
                'rating': Decimal('4.9'),
                'review_count': 67,
                'specifications': {
                    'Material': 'Full-grain leather',
                    'Capacity': '8 cards, cash',
                    'Dimensions': '4" x 3" x 0.5"',
                    'Color': 'Black, Brown'
                },
                'tags': ['leather', 'minimalist', 'wallet']
            },
            {
                'name': 'Ceramic Coffee Mug Set',
                'description': 'Beautiful set of 4 ceramic coffee mugs. Perfect for your morning routine.',
                'price': Decimal('49.99'),
                'category': 'Home & Garden',
                'stock_count': 40,
                'is_featured': True,
                'rating': Decimal('4.4'),
                'review_count': 92,
                'specifications': {
                    'Material': 'Ceramic',
                    'Capacity': '12 oz each',
                    'Set Size': '4 mugs',
                    'Dishwasher Safe': 'Yes'
                },
                'tags': ['ceramic', 'coffee', 'kitchen']
            }
        ]

        for product_data in products_data:
            category = categories[product_data['category']]
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults={
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
                self.stdout.write(f'Created product: {product.name}')
                
                # Add specifications
                for spec_name, spec_value in product_data.get('specifications', {}).items():
                    ProductSpecification.objects.create(
                        product=product,
                        name=spec_name,
                        value=spec_value
                    )
                
                # Add tags
                for tag_name in product_data.get('tags', []):
                    tag, _ = ProductTag.objects.get_or_create(name=tag_name)
                    product.tags.add(tag)

        # Create sample customers
        customers_data = [
            {
                'email': 'john.doe@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+1-555-0123',
                'status': 'active'
            },
            {
                'email': 'jane.smith@example.com',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+1-555-0456',
                'status': 'active'
            },
            {
                'email': 'mike.j@example.com',
                'first_name': 'Mike',
                'last_name': 'Johnson',
                'phone': '+1-555-0789',
                'status': 'vip'
            }
        ]

        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'Created customer: {customer.email}')

        self.stdout.write(
            self.style.SUCCESS('Successfully loaded sample data!')
        )
