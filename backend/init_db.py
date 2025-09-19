#!/usr/bin/env python
"""
Database initialization script for Railway deployment
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

def init_database():
    """Initialize the database with migrations and sample data"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipswich_retail.settings')
    django.setup()
    
    print("🔄 Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("🔄 Creating superuser...")
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@ipswichretail.com',
            password='admin123'
        )
        print("✅ Superuser created: admin/admin123")
    else:
        print("✅ Superuser already exists")
    
    print("🔄 Loading sample data...")
    execute_from_command_line(['manage.py', 'load_sample_data'])
    
    print("✅ Database initialization complete!")

if __name__ == '__main__':
    init_database()
