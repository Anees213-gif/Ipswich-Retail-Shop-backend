#!/bin/bash

# Exit on any error
set -e

echo "🚀 Starting Django application..."

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "🔄 Creating superuser..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@ipswichretail.com', 'admin123')
    print('✅ Superuser created: admin/admin123')
else:
    print('✅ Superuser already exists')
"

# Load sample data
echo "🔄 Loading sample data..."
python manage.py load_sample_data

# Start the server
echo "🚀 Starting Django server..."
python manage.py runserver 0.0.0.0:$PORT
