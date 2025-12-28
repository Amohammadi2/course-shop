from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ChatCategoryViewSet, UserChatTicketViewSet, AdminChatTicketViewSet
)

router = DefaultRouter()
router.register(r'categories', ChatCategoryViewSet, basename='chat-category')
router.register(r'tickets', UserChatTicketViewSet, basename='user-chat-ticket')
router.register(r'admin/tickets', AdminChatTicketViewSet, basename='admin-chat-ticket')

urlpatterns = [
    path('', include(router.urls)),
]
