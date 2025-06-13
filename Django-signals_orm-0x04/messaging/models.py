# messaging/models.py

from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messaging_received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_messages')
    read = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:30]}"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
