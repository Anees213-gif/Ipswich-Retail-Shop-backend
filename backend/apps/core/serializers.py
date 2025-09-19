from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active', 'product_count', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']
