from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a Message is saved, check if it's being edited.
    If the content changed, store old content in MessageHistory.
    """
    if not instance.pk:
        # New message, skip
        return

    # Get current database version
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content changed
    if old_message.content != instance.content:
        # Create history entry
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        # Mark the message as edited
        instance.edited = True
