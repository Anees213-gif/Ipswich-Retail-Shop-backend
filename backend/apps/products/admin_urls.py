from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_product_list_create, name='admin-product-list-create'),
    path('<int:pk>/', admin_views.AdminProductDetailView.as_view(), name='admin-product-detail'),
    path('<int:pk>/update/', admin_views.AdminProductUpdateView.as_view(), name='admin-product-update'),
    
    # Image upload endpoints
    path('<int:product_id>/images/', admin_views.admin_upload_product_image, name='admin-upload-product-image'),
    path('<int:product_id>/images/<int:image_id>/', admin_views.admin_delete_product_image, name='admin-delete-product-image'),
    path('<int:product_id>/images/<int:image_id>/set-primary/', admin_views.admin_set_primary_image, name='admin-set-primary-image'),
    path('<int:product_id>/images/reorder/', admin_views.admin_reorder_images, name='admin-reorder-images'),
]
