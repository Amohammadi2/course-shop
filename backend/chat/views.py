from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import ChatCategory, ChatTicket
from .serializers import (
    ChatCategorySerializer, ChatTicketSerializer, CreateChatTicketSerializer
)

@extend_schema(summary="List all chat categories")
class ChatCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ChatCategory.objects.all()
    serializer_class = ChatCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(summary="Manage the current user's chat tickets")
class UserChatTicketViewSet(viewsets.ModelViewSet):
    serializer_class = ChatTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ChatTicket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        category = serializer.validated_data['category']
        admin = ChatTicket.assign_admin(category)
        serializer.save(user=self.request.user, assigned_admin=admin)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateChatTicketSerializer
        return ChatTicketSerializer

@extend_schema(summary="Admin: Manage all chat tickets")
class AdminChatTicketViewSet(viewsets.ModelViewSet):
    queryset = ChatTicket.objects.all()
    serializer_class = ChatTicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return ChatTicket.objects.filter(assigned_admin=self.request.user)
