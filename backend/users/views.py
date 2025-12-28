from rest_framework import generics, viewsets, permissions
from drf_spectacular.utils import extend_schema
from .models import User
from .serializers import UserSerializer, UserRegistrationSerializer

@extend_schema(
    summary="Register a new user",
    description="Create a new user account. Open to any unauthenticated user."
)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(
    summary="Retrieve or update the current user's profile",
    description="Allows an authenticated user to view and update their own profile details."
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema(
    summary="Admin-only user management",
    description="Provides full CRUD (Create, Read, Update, Delete) capabilities for user accounts. Restricted to admin users."
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
