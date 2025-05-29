from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


# Create your models here.
# chats/models.py


class CustomUser(AbstractUser):
    # Add any custom fields you need here (optional for now)
    # Example: phone_number = models.CharField(max_length=15, blank=True, null=True)
    pass

class Conversation(models.Model):
    participants = models.ManyToManyField('CustomUser', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Message(models.Model):
    conversation = models.ForeignKey("Conversation", related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username}: {self.text[:30]}"
