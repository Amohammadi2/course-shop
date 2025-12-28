from rest_framework import serializers
from .models import ChatCategory, ChatTicket, ChatMessage
from users.serializers import UserSerializer

class ChatCategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatCategory model.
    """
    class Meta:
        model = ChatCategory
        fields = ('id', 'name')

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatMessage model.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ('id', 'sender', 'message', 'timestamp')

class ChatTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for the ChatTicket model.
    """
    user = UserSerializer(read_only=True)
    assigned_admin = UserSerializer(read_only=True)
    category = ChatCategorySerializer(read_only=True)
    messages = ChatMessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatTicket
        fields = ('id', 'user', 'assigned_admin', 'category', 'status', 'created_at', 'messages')

class CreateChatTicketSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new chat ticket.
    """
    class Meta:
        model = ChatTicket
        fields = ('category',)
