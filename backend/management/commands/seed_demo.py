"""
Management command to seed demo data for development and testing
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.core.models import Category
from apps.products.models import Product, ProductImage, ProductSpecification, ProductTag
from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed demo data for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            OrderItem.objects.all().delete()
            Order.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            Customer.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Seeding demo data...')

        # Create admin user
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@ipswichretail.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write('✅ Created admin user: admin@ipswichretail.com / admin123')
        else:
            self.stdout.write('📁 Admin user already exists')

        # Create categories
        categories_data = [
            {'name': 'Electronics', 'description': 'Latest tech gadgets and devices'},
            {'name': 'Apparel', 'description': 'Fashion and clothing for all'},
            {'name': 'Home & Garden', 'description': 'Everything for your home and garden'},
            {'name': 'Sports & Outdoors', 'description': 'Sports equipment and outdoor gear'},
            {'name': 'Books & Media', 'description': 'Books, movies, and digital media'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'✅ Created category: {category.name}')

        # Create products with brands
        products_data = [
            {
                'name': 'Premium Wireless Headphones',
                'brand': 'Sony',
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
                'name': 'Smart Fitness Watch',
                'brand': 'Apple',
                'description': 'Advanced fitness tracking with heart rate monitoring, GPS, and 7-day battery life.',
                'price': Decimal('199.99'),
                'original_price': Decimal('249.99'),
                'category': 'Electronics',
                'stock_count': 40,
                'is_featured': True,
                'rating': Decimal('4.6'),
                'review_count': 89,
                'specifications': {
                    'Battery Life': '7 days',
                    'Water Resistance': '5ATM',
                    'Display': '1.4" AMOLED',
                    'Sensors': 'Heart Rate, GPS, Accelerometer'
                },
                'tags': ['fitness', 'smartwatch', 'health']
            },
            {
                'name': '4K Ultra HD TV 55"',
                'brand': 'Samsung',
                'description': 'Stunning 4K picture quality with HDR support and smart TV features.',
                'price': Decimal('899.99'),
                'original_price': Decimal('1199.99'),
                'category': 'Electronics',
                'stock_count': 15,
                'is_featured': True,
                'rating': Decimal('4.7'),
                'review_count': 234,
                'specifications': {
                    'Screen Size': '55 inches',
                    'Resolution': '4K Ultra HD (3840x2160)',
                    'HDR': 'HDR10, Dolby Vision',
                    'Smart TV': 'Built-in'
                },
                'tags': ['4k', 'smart-tv', 'hdr']
            },
            {
                'name': 'Organic Cotton T-Shirt',
                'brand': 'Patagonia',
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
                'name': 'Premium Denim Jeans',
                'brand': 'Levi\'s',
                'description': 'Classic fit denim jeans made from premium cotton with a comfortable stretch.',
                'price': Decimal('89.99'),
                'original_price': Decimal('120.00'),
                'category': 'Apparel',
                'stock_count': 30,
                'is_featured': False,
                'rating': Decimal('4.3'),
                'review_count': 67,
                'specifications': {
                    'Material': '98% Cotton, 2% Elastane',
                    'Fit': 'Classic',
                    'Rise': 'Mid-rise'
                },
                'tags': ['denim', 'jeans', 'classic']
            },
            {
                'name': 'Smart Home Security Camera',
                'brand': 'Ring',
                'description': 'Wireless security camera with night vision, motion detection, and mobile app control.',
                'price': Decimal('149.99'),
                'original_price': Decimal('199.99'),
                'category': 'Home & Garden',
                'stock_count': 20,
                'is_featured': True,
                'rating': Decimal('4.4'),
                'review_count': 123,
                'specifications': {
                    'Resolution': '1080p HD',
                    'Night Vision': '30ft range',
                    'Storage': 'Cloud & Local',
                    'Connectivity': 'WiFi'
                },
                'tags': ['security', 'smart-home', 'camera']
            },
            {
                'name': 'Indoor Plant Collection',
                'brand': 'Costa Farms',
                'description': 'Beautiful collection of easy-care indoor plants perfect for home decoration.',
                'price': Decimal('79.99'),
                'category': 'Home & Garden',
                'stock_count': 35,
                'is_featured': False,
                'rating': Decimal('4.6'),
                'review_count': 45,
                'specifications': {
                    'Plants Included': '5 different varieties',
                    'Pot Material': 'Ceramic',
                    'Care Level': 'Easy'
                },
                'tags': ['plants', 'indoor', 'decorative']
            },
            {
                'name': 'Professional Yoga Mat',
                'brand': 'Lululemon',
                'description': 'Non-slip yoga mat with excellent grip and cushioning for all yoga practices.',
                'price': Decimal('59.99'),
                'original_price': Decimal('79.99'),
                'category': 'Sports & Outdoors',
                'stock_count': 60,
                'is_featured': True,
                'rating': Decimal('4.7'),
                'review_count': 178,
                'specifications': {
                    'Material': 'TPE (Thermoplastic Elastomer)',
                    'Thickness': '6mm',
                    'Size': '72" x 24"',
                    'Weight': '2.5 lbs'
                },
                'tags': ['yoga', 'fitness', 'non-slip']
            },
            {
                'name': 'Camping Tent 4-Person',
                'brand': 'Coleman',
                'description': 'Spacious 4-person tent with weather protection and easy setup.',
                'price': Decimal('199.99'),
                'original_price': Decimal('279.99'),
                'category': 'Sports & Outdoors',
                'stock_count': 12,
                'is_featured': False,
                'rating': Decimal('4.5'),
                'review_count': 92,
                'specifications': {
                    'Capacity': '4 people',
                    'Weight': '8.5 lbs',
                    'Setup Time': '10 minutes',
                    'Weather Protection': 'Waterproof'
                },
                'tags': ['camping', 'tent', 'outdoor']
            },
            {
                'name': 'Programming Fundamentals Book',
                'brand': 'O\'Reilly',
                'description': 'Comprehensive guide to programming fundamentals with practical examples.',
                'price': Decimal('49.99'),
                'category': 'Books & Media',
                'stock_count': 80,
                'is_featured': True,
                'rating': Decimal('4.8'),
                'review_count': 156,
                'specifications': {
                    'Pages': '450',
                    'Format': 'Paperback',
                    'Language': 'English',
                    'Publisher': 'O\'Reilly Media'
                },
                'tags': ['programming', 'education', 'book']
            },
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
                    'brand': product_data.get('brand', ''),
                    'stock_count': product_data['stock_count'],
                    'is_featured': product_data['is_featured'],
                    'rating': product_data['rating'],
                    'review_count': product_data['review_count'],
                }
            )
            
            if created:
                self.stdout.write(f'✅ Created product: {product.name}')
                
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

        # Create demo customers
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
            },
            {
                'email': 'sarah.w@example.com',
                'first_name': 'Sarah',
                'last_name': 'Wilson',
                'phone': '+1-555-0321',
                'status': 'active'
            },
            {
                'email': 'david.brown@example.com',
                'first_name': 'David',
                'last_name': 'Brown',
                'phone': '+1-555-0654',
                'status': 'inactive'
            }
        ]

        for customer_data in customers_data:
            customer, created = Customer.objects.get_or_create(
                email=customer_data['email'],
                defaults=customer_data
            )
            if created:
                self.stdout.write(f'✅ Created customer: {customer.email}')

        # Create sample orders
        customers = Customer.objects.all()
        products = Product.objects.all()
        
        if customers.exists() and products.exists():
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
                    shipping_address_line1=customer.address_line1 or '123 Main St',
                    shipping_city=customer.city or 'Boston',
                    shipping_state=customer.state or 'MA',
                    shipping_zip_code=customer.zip_code or '02101',
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
                
                self.stdout.write(f'✅ Created order: {order.order_number} - ${order.total_amount}')

        self.stdout.write(
            self.style.SUCCESS('✅ Successfully seeded demo data!')
        )
        self.stdout.write(f'📊 Summary:')
        self.stdout.write(f'   - Categories: {Category.objects.count()}')
        self.stdout.write(f'   - Products: {Product.objects.count()}')
        self.stdout.write(f'   - Customers: {Customer.objects.count()}')
        self.stdout.write(f'   - Orders: {Order.objects.count()}')
        self.stdout.write(f'   - Order Items: {OrderItem.objects.count()}')
