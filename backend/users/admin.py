from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Customizes the admin interface for the User model.
    Extends the default UserAdmin to add more display columns, filters,
    and search capabilities, making user management more efficient.
    """
    # Columns to display in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    # Filters available on the side of the user list
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    # Fields to search by
    search_fields = ('username', 'first_name', 'last_name', 'email')
    # Default ordering of the user list
    ordering = ('-date_joined',)

    # Customize the fieldsets for the user edit page (optional but good practice)
    # This keeps the layout familiar by inheriting from the base UserAdmin
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ()}), # Add custom fields here if any
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (None, {'fields': ()}), # Add custom fields here if any
    )
