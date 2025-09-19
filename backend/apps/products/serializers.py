from rest_framework import serializers
from django.conf import settings
from .models import Product, ProductImage, ProductSpecification, ProductTag
from apps.core.serializers import CategorySerializer


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'image_url', 'alt_text', 'is_primary', 'order']
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return f"{settings.MEDIA_URL}{obj.image}"
        return None


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['name', 'value']


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = ['id', 'name', 'slug']


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image = serializers.SerializerMethodField()
    in_stock = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    tags = ProductTagSerializer(many=True, read_only=True)
    # Convert ID to string for frontend compatibility
    id = serializers.CharField(read_only=True)
    # Convert prices to strings for consistent decimal handling
    price = serializers.CharField(read_only=True)
    original_price = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'original_price',
            'category', 'brand', 'stock_count', 'is_active', 'is_featured', 'rating',
            'review_count', 'in_stock', 'discount_percentage', 'primary_image',
            'tags', 'created_at'
        ]

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image).data
        # Fallback to first image if no primary image
        first_image = obj.images.first()
        if first_image:
            return ProductImageSerializer(first_image).data
        return None


class ProductDetailSerializer(ProductListSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + ['images', 'specifications']


class AdminProductSerializer(serializers.ModelSerializer):
    """Admin serializer for creating and updating products"""
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    primary_image = serializers.SerializerMethodField()
    in_stock = serializers.ReadOnlyField()
    discount_percentage = serializers.ReadOnlyField()
    tags = ProductTagSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'original_price',
            'category', 'category_id', 'brand', 'stock_count', 'is_active', 
            'is_featured', 'rating', 'review_count', 'in_stock', 
            'discount_percentage', 'primary_image', 'tags', 'created_at'
        ]

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return ProductImageSerializer(primary_image, context=self.context).data
        # Fallback to first image if no primary image
        first_image = obj.images.first()
        if first_image:
            return ProductImageSerializer(first_image, context=self.context).data
        return None

    def create(self, validated_data):
        print(f"Creating product with validated_data: {validated_data}")
        category_id = validated_data.pop('category_id')
        from apps.core.models import Category
        category = Category.objects.get(id=category_id)
        validated_data['category'] = category
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'category_id' in validated_data:
            category_id = validated_data.pop('category_id')
            from apps.core.models import Category
            category = Category.objects.get(id=category_id)
            validated_data['category'] = category
        return super().update(instance, validated_data)
