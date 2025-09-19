from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import json
import os
from PIL import Image
from .models import Product, ProductImage
from .serializers import ProductDetailSerializer, ProductListSerializer, AdminProductSerializer


class AdminProductListView(generics.ListCreateAPIView):
    """
    List all products or create a new product for admin panel
    """
    queryset = Product.objects.all().select_related('category').prefetch_related('images', 'tags')
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]


class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a product for admin panel
    """
    queryset = Product.objects.all().select_related('category').prefetch_related('images', 'tags')
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]


class AdminProductUpdateView(generics.UpdateAPIView):
    """
    Update a product for admin panel
    """
    queryset = Product.objects.all()
    serializer_class = AdminProductSerializer
    permission_classes = [IsAdminUser]


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def admin_product_list_create(request):
    """
    List all products (GET) or create a new product (POST) for admin panel
    """
    if request.method == 'GET':
        # List products
        products = Product.objects.all().select_related('category').prefetch_related('images', 'tags')
        serializer = AdminProductSerializer(products, many=True, context={'request': request})
        return Response({
            'products': serializer.data,
            'meta': {
                'total': products.count(),
                'page': 1,
                'pageSize': 20,
                'totalPages': 1
            }
        })
    
    elif request.method == 'POST':
        # Create product using DRF serializer
        print(f"Received data: {request.data}")
        serializer = AdminProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            product = serializer.save()
            return Response(AdminProductSerializer(product, context={'request': request}).data, status=status.HTTP_201_CREATED)
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_upload_product_image(request, product_id):
    """
    Upload an image for a specific product
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        
        if 'image' not in request.FILES:
            return Response({'error': 'No image file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        image_file = request.FILES['image']
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
        if image_file.content_type not in allowed_types:
            return Response({
                'error': f'Invalid file type. Allowed types: {", ".join(allowed_types)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate file size (max 5MB)
        max_size = 5 * 1024 * 1024  # 5MB
        if image_file.size > max_size:
            return Response({
                'error': 'File size too large. Maximum size is 5MB'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Generate filename
        file_extension = os.path.splitext(image_file.name)[1]
        filename = f"products/{product.slug}_{product.images.count() + 1}{file_extension}"
        
        # Save the file
        file_path = default_storage.save(filename, ContentFile(image_file.read()))
        
        # Create ProductImage record
        alt_text = request.data.get('alt_text', f"{product.name} image")
        is_primary = request.data.get('is_primary', False)
        
        # If this is set as primary, unset other primary images
        if is_primary:
            ProductImage.objects.filter(product=product, is_primary=True).update(is_primary=False)
        
        product_image = ProductImage.objects.create(
            product=product,
            image=file_path,
            alt_text=alt_text,
            is_primary=is_primary,
            order=product.images.count() + 1
        )
        
        return Response({
            'id': product_image.id,
            'image': product_image.image.url,
            'alt_text': product_image.alt_text,
            'is_primary': product_image.is_primary,
            'order': product_image.order
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_delete_product_image(request, product_id, image_id):
    """
    Delete a specific product image
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        product_image = get_object_or_404(ProductImage, id=image_id, product=product)
        
        # Delete the file from storage
        if product_image.image:
            default_storage.delete(product_image.image.name)
        
        # Delete the database record
        product_image.delete()
        
        return Response({'message': 'Image deleted successfully'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_set_primary_image(request, product_id, image_id):
    """
    Set a specific image as the primary image for a product
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        product_image = get_object_or_404(ProductImage, id=image_id, product=product)
        
        # Unset all other primary images for this product
        ProductImage.objects.filter(product=product, is_primary=True).update(is_primary=False)
        
        # Set this image as primary
        product_image.is_primary = True
        product_image.save()
        
        return Response({'message': 'Primary image updated successfully'}, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def admin_reorder_images(request, product_id):
    """
    Reorder images for a product
    """
    try:
        product = get_object_or_404(Product, id=product_id)
        data = json.loads(request.body)
        
        if 'image_orders' not in data:
            return Response({'error': 'image_orders field is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update the order of each image
        for image_data in data['image_orders']:
            image_id = image_data.get('id')
            order = image_data.get('order')
            
            if image_id and order is not None:
                ProductImage.objects.filter(id=image_id, product=product).update(order=order)
        
        return Response({'message': 'Images reordered successfully'}, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError as e:
        return Response({'error': f'Invalid JSON: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)