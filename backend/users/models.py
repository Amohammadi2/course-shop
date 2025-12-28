from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    This model is the central point for user authentication and identification.
    It includes all the fields from AbstractUser (username, email, password, etc.)
    and can be extended with additional profile fields in the future.
    """
    # You can add additional fields here if needed in the future.
    # For example:
    # bio = models.TextField(blank=True)
    # avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username
