import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from reconnect.models import Conversation, Message, ConversationParticipant


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for real-time synchronised chat.
    URL: ws/chat/<conversation_id>/
    """

    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f'chat_{self.conversation_id}'
        self.user = self.scope['user']

        # Reject anonymous users
        if self.user.is_anonymous:
            await self.close()
            return

        # Verify user is a participant
        is_participant = await self.check_participant()
        if not is_participant:
            await self.close()
            return

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data.get('message', '').strip()
        if not message_content:
            return

        # Save to database
        msg = await self.save_message(message_content)

        # Broadcast to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_content,
                'sender_id': self.user.id,
                'sender_name': self.user.get_full_name() or self.user.username,
                'sender_initials': self.user.get_initials(),
                'message_id': str(msg.id),
                'timestamp': msg.timestamp.strftime('%H:%M'),
            },
        )

    async def chat_message(self, event):
        """Handler for messages broadcast to the group."""
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'sender_initials': event['sender_initials'],
            'message_id': event['message_id'],
            'timestamp': event['timestamp'],
        }))

    # ─── Database helpers ─────────────────────────────────────────────────

    @database_sync_to_async
    def check_participant(self):
        return ConversationParticipant.objects.filter(
            conversation_id=self.conversation_id,
            user=self.user,
        ).exists()

    @database_sync_to_async
    def save_message(self, content):
        conversation = Conversation.objects.get(id=self.conversation_id)
        return Message.objects.create(
            conversation=conversation,
            sender=self.user,
            content=content,
        )
