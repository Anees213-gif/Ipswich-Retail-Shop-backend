"""
Tests for core app
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.db import connection

from .models import Category


class CategoryModelTest(TestCase):
    """Test Category model"""
    
    def test_category_creation(self):
        """Test category creation"""
        category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
        
        self.assertEqual(category.name, 'Electronics')
        self.assertEqual(category.slug, 'electronics')
        self.assertEqual(category.description, 'Electronic devices and gadgets')
        self.assertTrue(category.is_active)
    
    def test_category_slug_generation(self):
        """Test automatic slug generation"""
        category = Category.objects.create(
            name='Home & Garden',
            description='Home and garden products'
        )
        
        self.assertEqual(category.slug, 'home-garden')
    
    def test_category_product_count_property(self):
        """Test product_count property"""
        category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        
        # Initially no products
        self.assertEqual(category.product_count, 0)
        
        # Add a product (we'll need to import Product model for this)
        from apps.products.models import Product
        product = Product.objects.create(
            name='Test Product',
            description='Test description',
            price=100.00,
            category=category,
            stock_count=10
        )
        
        # Refresh from database
        category.refresh_from_db()
        self.assertEqual(category.product_count, 1)


class CategoryAPITest(APITestCase):
    """Test Category API endpoints"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic devices and gadgets'
        )
    
    def test_category_list_api(self):
        """Test category list API endpoint"""
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        category_data = response.data['results'][0]
        self.assertEqual(category_data['name'], 'Electronics')
        self.assertEqual(category_data['slug'], 'electronics')
        self.assertEqual(category_data['description'], 'Electronic devices and gadgets')
    
    def test_category_detail_api(self):
        """Test category detail API endpoint"""
        url = reverse('category-detail', kwargs={'pk': self.category.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Electronics')
        self.assertEqual(response.data['slug'], 'electronics')
    
    def test_category_filtering(self):
        """Test category filtering"""
        # Create another category
        Category.objects.create(
            name='Books',
            description='Books and media'
        )
        
        url = reverse('category-list')
        response = self.client.get(url, {'name': 'Electronics'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Electronics')
    
    def test_category_search(self):
        """Test category search functionality"""
        url = reverse('category-list')
        response = self.client.get(url, {'search': 'Electronic'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Electronics')


class HealthCheckAPITest(APITestCase):
    """Test health check API endpoint"""
    
    def test_health_check_endpoint(self):
        """Test health check endpoint returns healthy status"""
        url = reverse('health-check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')
        self.assertEqual(response.data['version'], '1.0.0')
        self.assertIn('timestamp', response.data)
        self.assertIn('database', response.data)
        self.assertIn('services', response.data)
    
    def test_health_check_database_connection(self):
        """Test health check includes database status"""
        url = reverse('health-check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['database'], 'connected')
        self.assertEqual(response.data['services']['database'], 'connected')
    
    def test_health_check_system_info(self):
        """Test health check includes system information"""
        url = reverse('health-check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('system', response.data)
        self.assertIn('environment', response.data)


class MetricsAPITest(APITestCase):
    """Test metrics API endpoint"""
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint returns Prometheus format"""
        url = reverse('metrics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/plain')
        
        # Check that response contains metrics data
        metrics_text = response.content.decode('utf-8')
        self.assertIn('application_info', metrics_text)
        self.assertIn('products_total', metrics_text)
        self.assertIn('orders_total', metrics_text)
        self.assertIn('customers_total', metrics_text)
    
    def test_metrics_includes_product_counts(self):
        """Test metrics includes product-related counts"""
        # Create some test data
        category = Category.objects.create(
            name='Electronics',
            description='Electronic devices'
        )
        
        from apps.products.models import Product
        Product.objects.create(
            name='Test Product 1',
            description='Test description',
            price=100.00,
            category=category,
            stock_count=10,
            is_active=True,
            is_featured=True
        )
        Product.objects.create(
            name='Test Product 2',
            description='Test description',
            price=200.00,
            category=category,
            stock_count=5,
            is_active=True,
            is_featured=False
        )
        
        url = reverse('metrics')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        metrics_text = response.content.decode('utf-8')
        
        self.assertIn('products_total 2', metrics_text)
        self.assertIn('products_active 2', metrics_text)
        self.assertIn('products_featured 1', metrics_text)


class APIRootTest(APITestCase):
    """Test API root endpoint"""
    
    def test_api_root_endpoint(self):
        """Test API root endpoint returns welcome message and endpoints"""
        url = reverse('api-root')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Welcome to Ipswich Retail API')
        self.assertEqual(response.data['version'], '1.0.0')
        self.assertEqual(response.data['status'], 'healthy')
        self.assertIn('endpoints', response.data)
        
        endpoints = response.data['endpoints']
        self.assertIn('categories', endpoints)
        self.assertIn('products', endpoints)
        self.assertIn('orders', endpoints)
        self.assertIn('customers', endpoints)
        self.assertIn('admin', endpoints)
