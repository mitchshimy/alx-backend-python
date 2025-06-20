from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save

@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )
User = get_user_model()
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    print(f"[Signal] Deleting data for user: {instance}")
    # If not using CASCADE, manually delete:
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    Notification.objects.filter(user=instance).delete()
    MessageHistory.objects.filter(message__sender=instance).delete()

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_message = Message.objects.get(pk=instance.pk)
            if old_message.content != instance.content:
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass