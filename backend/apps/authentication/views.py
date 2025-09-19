from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.http import JsonResponse
import json


@csrf_exempt
def admin_login(request):
    """
    Admin login endpoint - CSRF exempt
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    if not email or not password:
        return JsonResponse(
            {'error': 'Email and password are required'}, 
            status=400
        )
    
    # Find user by email
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return JsonResponse(
            {'error': 'Invalid credentials'}, 
            status=401
        )
    
    # Authenticate user
    user = authenticate(username=user.username, password=password)
    if user and user.is_staff:
        login(request, user)
        # Force session save
        request.session.save()
        return JsonResponse({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'is_staff': user.is_staff,
            }
        })
    else:
        return JsonResponse(
            {'error': 'Invalid credentials'}, 
            status=401
        )


@csrf_exempt
def admin_logout(request):
    """
    Admin logout endpoint - CSRF exempt
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    logout(request)
    return JsonResponse({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([AllowAny])
def admin_csrf_token(request):
    """
    Get CSRF token for API requests
    """
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})


@csrf_exempt
def admin_user_info(request):
    """
    Get current admin user info - CSRF exempt
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    user = request.user
    return JsonResponse({
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'is_staff': user.is_staff,
        'is_authenticated': user.is_authenticated,
    })
