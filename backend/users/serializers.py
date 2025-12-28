from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    Used for retrieving and updating user information. It exposes a safe subset of
    the user's fields, excluding sensitive data like the password.
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ('id',)

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new User instances.
    It handles the validation of input data, including the password, and creates
    a new user. The password field is write-only, ensuring it's never exposed
    in API responses.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

    def create(self, validated_data):
        """
        Create and return a new User instance, given the validated data.
        This method hashes the password before saving the user to the database.
        """
        user = User.objects.create_user(**validated_data)
        return user
