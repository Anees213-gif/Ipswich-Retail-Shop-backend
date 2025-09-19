from django.urls import path
from . import views

urlpatterns = [
    path('csrf/', views.admin_csrf_token, name='admin-csrf-token'),
    path('login/', views.admin_login, name='admin-login'),
    path('logout/', views.admin_logout, name='admin-logout'),
    path('user/', views.admin_user_info, name='admin-user-info'),
]
