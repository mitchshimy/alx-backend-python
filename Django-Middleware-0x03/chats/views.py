# chats/views.py

from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation  # ✅ import permission
from rest_framework.permissions import IsAuthenticated
from .filters import MessageFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import NotAuthenticated


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['conversation_id']

    def get_queryset(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to access conversations.")
        return Conversation.objects.filter(participants=user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
