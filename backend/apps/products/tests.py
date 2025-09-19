"""
Tests for products app
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Product, ProductImage, ProductSpecification, ProductTag
from apps.core.models import Category


class ProductModelTest(TestCase):
    """Test Product model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            brand='Test Brand',
            stock_count=10
        )
    
    def test_product_creation(self):
        """Test product creation"""
        self.assertEqual(self.product.name, 'Test Product')
        self.assertEqual(self.product.brand, 'Test Brand')
        self.assertEqual(self.product.stock_count, 10)
        self.assertTrue(self.product.in_stock)
    
    def test_product_slug_generation(self):
        """Test automatic slug generation"""
        self.assertEqual(self.product.slug, 'test-product')
    
    def test_discount_percentage_calculation(self):
        """Test discount percentage calculation"""
        self.product.original_price = Decimal('149.99')
        self.product.save()
        
        expected_discount = round(((149.99 - 99.99) / 149.99) * 100)
        self.assertEqual(self.product.discount_percentage, expected_discount)
    
    def test_in_stock_property(self):
        """Test in_stock property"""
        self.assertTrue(self.product.in_stock)
        
        self.product.stock_count = 0
        self.product.save()
        self.assertFalse(self.product.in_stock)


class ProductAPITest(APITestCase):
    """Test Product API endpoints"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            original_price=Decimal('149.99'),
            category=self.category,
            brand='Test Brand',
            stock_count=10,
            is_featured=True,
            rating=Decimal('4.5'),
            review_count=100
        )
        
        # Create admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True
        )
    
    def test_product_list_api(self):
        """Test product list API endpoint"""
        url = reverse('product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        product_data = response.data['results'][0]
        self.assertEqual(product_data['name'], 'Test Product')
        self.assertEqual(product_data['brand'], 'Test Brand')
        self.assertEqual(product_data['price'], '99.99')  # Should be string
        self.assertEqual(product_data['original_price'], '149.99')  # Should be string
        self.assertTrue(product_data['in_stock'])
        self.assertTrue(product_data['is_featured'])
    
    def test_product_detail_api(self):
        """Test product detail API endpoint"""
        url = reverse('product-detail', kwargs={'slug': self.product.slug})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')
        self.assertEqual(response.data['brand'], 'Test Brand')
        self.assertEqual(response.data['price'], '99.99')
    
    def test_product_filtering_by_category(self):
        """Test product filtering by category"""
        url = reverse('product-list')
        response = self.client.get(url, {'category': self.category.id})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_product_filtering_by_brand(self):
        """Test product filtering by brand"""
        url = reverse('product-list')
        response = self.client.get(url, {'brand': 'Test Brand'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_product_search(self):
        """Test product search functionality"""
        url = reverse('product-list')
        response = self.client.get(url, {'search': 'Test'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_product_ordering(self):
        """Test product ordering"""
        # Create another product
        Product.objects.create(
            name='Another Product',
            description='Another description',
            price=Decimal('199.99'),
            category=self.category,
            brand='Another Brand',
            stock_count=5
        )
        
        url = reverse('product-list')
        response = self.client.get(url, {'ordering': 'price'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        # First product should have lower price
        self.assertEqual(response.data['results'][0]['price'], '99.99')
    
    def test_product_pagination(self):
        """Test product pagination"""
        # Create multiple products
        for i in range(25):
            Product.objects.create(
                name=f'Product {i}',
                description=f'Description {i}',
                price=Decimal('99.99'),
                category=self.category,
                brand=f'Brand {i}',
                stock_count=10
            )
        
        url = reverse('product-list')
        response = self.client.get(url, {'page_size': 10})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)
        self.assertEqual(response.data['meta']['pageSize'], 10)
        self.assertEqual(response.data['meta']['totalItems'], 26)  # 25 new + 1 existing
        self.assertTrue(response.data['meta']['hasNext'])
    
    def test_product_creation_requires_auth(self):
        """Test that product creation requires authentication"""
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'New description',
            'price': '199.99',
            'category': self.category.id,
            'brand': 'New Brand',
            'stock_count': 5
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_creation_with_auth(self):
        """Test product creation with authentication"""
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('product-create')
        data = {
            'name': 'New Product',
            'description': 'New description',
            'price': '199.99',
            'category': self.category.id,
            'brand': 'New Brand',
            'stock_count': 5
        }
        
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Product')
        self.assertEqual(response.data['brand'], 'New Brand')
    
    def test_product_update_requires_auth(self):
        """Test that product update requires authentication"""
        url = reverse('product-update', kwargs={'slug': self.product.slug})
        data = {'price': '89.99'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_product_update_with_auth(self):
        """Test product update with authentication"""
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('product-update', kwargs={'slug': self.product.slug})
        data = {'price': '89.99'}
        
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['price'], '89.99')


class ProductSpecificationTest(TestCase):
    """Test ProductSpecification model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            brand='Test Brand',
            stock_count=10
        )
    
    def test_specification_creation(self):
        """Test product specification creation"""
        spec = ProductSpecification.objects.create(
            product=self.product,
            name='Color',
            value='Black'
        )
        
        self.assertEqual(spec.product, self.product)
        self.assertEqual(spec.name, 'Color')
        self.assertEqual(spec.value, 'Black')
    
    def test_specification_unique_constraint(self):
        """Test that specifications are unique per product"""
        ProductSpecification.objects.create(
            product=self.product,
            name='Color',
            value='Black'
        )
        
        # Try to create another specification with same name for same product
        with self.assertRaises(Exception):
            ProductSpecification.objects.create(
                product=self.product,
                name='Color',
                value='White'
            )


class ProductTagTest(TestCase):
    """Test ProductTag model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        self.product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            brand='Test Brand',
            stock_count=10
        )
    
    def test_tag_creation(self):
        """Test product tag creation"""
        tag = ProductTag.objects.create(name='wireless')
        
        self.assertEqual(tag.name, 'wireless')
        self.assertEqual(tag.slug, 'wireless')
    
    def test_tag_slug_generation(self):
        """Test automatic slug generation for tags"""
        tag = ProductTag.objects.create(name='Noise Cancelling')
        
        self.assertEqual(tag.slug, 'noise-cancelling')
    
    def test_tag_product_relationship(self):
        """Test many-to-many relationship between tags and products"""
        tag1 = ProductTag.objects.create(name='wireless')
        tag2 = ProductTag.objects.create(name='premium')
        
        self.product.tags.add(tag1, tag2)
        
        self.assertEqual(self.product.tags.count(), 2)
        self.assertIn(tag1, self.product.tags.all())
        self.assertIn(tag2, self.product.tags.all())
