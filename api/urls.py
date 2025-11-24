from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from . import viewsets, views

app_name = 'api'

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', viewsets.PostViewSet, basename='post')
router.register(r'users', viewsets.UserViewSet, basename='user')
router.register(r'comments', viewsets.CommentViewSet, basename='comment')
router.register(r'notifications', viewsets.NotificationViewSet, basename='notification')

urlpatterns = [
    # JWT Authentication endpoints
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/register/', views.register, name='register'),
    path('auth/me/', views.current_user, name='current_user'),
    
    # Include router URLs
    path('', include(router.urls)),
]