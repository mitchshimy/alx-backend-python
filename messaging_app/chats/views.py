from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['conversation_id']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically include the current user as a participant
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return messages in conversations the user is part of
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the sender as the current user
        serializer.save(sender=self.request.user)
