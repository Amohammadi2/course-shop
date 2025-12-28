from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationView, UserProfileView, UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls)),
]
