from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product-list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('create/', views.ProductCreateView.as_view(), name='product-create'),
    path('<slug:slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
]
