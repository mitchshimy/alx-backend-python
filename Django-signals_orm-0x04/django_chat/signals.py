from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models.signals import post_delete
from .models import Message, MessageHistory
from django.contrib.auth import get_user_model

@receiver(pre_save, sender=Message)
def log_message_edits(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, skip

    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old_message.content != instance.content:
        MessageHistory.objects.create(
            message=old_message,
            old_content=old_message.content
        )
        instance.edited = True

User = get_user_model()
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    print(f"[Signal] Deleting data for user: {instance}")
    # If not using CASCADE, manually delete:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()