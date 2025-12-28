import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatTicket, ChatMessage, User

class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat sessions.
    It manages WebSocket connections, message broadcasting, and message
    persistence.
    """
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.ticket_group_name = f'chat_{self.ticket_id}'
        self.user = self.scope['user']

        if self.user.is_anonymous:
            await self.close()
            return

        is_authorized = await self.is_user_authorized(self.user, self.ticket_id)
        if not is_authorized:
            await self.close()
            return

        await self.channel_layer.group_add(
            self.ticket_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.ticket_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_text = text_data_json['message']

        message = await self.create_message(message_text)

        await self.channel_layer.group_send(
            self.ticket_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': self.user.username,
                'timestamp': str(message.timestamp)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def is_user_authorized(self, user, ticket_id):
        """
        Checks if a user is authorized to join a chat ticket.
        """
        try:
            ticket = ChatTicket.objects.get(id=ticket_id)
            if user.is_staff:
                return ticket.assigned_admin == user
            else:
                return ticket.user == user
        except ChatTicket.DoesNotExist:
            return False

    @database_sync_to_async
    def create_message(self, message_text):
        """
        Saves a new chat message to the database.
        """
        ticket = ChatTicket.objects.get(id=self.ticket_id)
        return ChatMessage.objects.create(
            ticket=ticket,
            sender=self.user,
            message=message_text
        )
