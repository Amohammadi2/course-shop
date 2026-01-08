from django.contrib import admin
from .models import ChatCategory, ChatTicket, ChatMessage

@admin.register(ChatCategory)
class ChatCategoryAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the ChatCategory model.
    Improves management of chat categories with search and a
    user-friendly interface for assigning admins.
    """
    list_display = ('name',)
    search_fields = ('name',)
    filter_horizontal = ('admins',)

@admin.register(ChatTicket)
class ChatTicketAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the ChatTicket model.
    Provides a comprehensive view of support tickets, enabling efficient
    tracking, assignment, and review with advanced search and filtering.
    """
    list_display = ('id', 'user', 'assigned_admin', 'category', 'status', 'created_at')
    search_fields = ('id', 'user__username', 'assigned_admin__username', 'category__name')
    list_filter = ('status', 'category', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'created_at', 'updated_at')
    autocomplete_fields = ('user', 'assigned_admin', 'category')

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the ChatMessage model.
    Displays chat messages in a read-only format to ensure the integrity
    of the conversation history.
    """
    list_display = ('ticket', 'sender', 'timestamp')
    search_fields = ('ticket__id', 'sender__username', 'message')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
    readonly_fields = ('ticket', 'sender', 'message', 'timestamp')

    def has_add_permission(self, request):
        # Messages should be created via the chat interface, not manually
        return False

    def has_delete_permission(self, request, obj=None):
        # Messages should not be deleted to maintain conversation history
        return False
