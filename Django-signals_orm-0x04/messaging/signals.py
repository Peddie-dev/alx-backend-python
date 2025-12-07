from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    """
    Before a Message is saved, log old content if the message is being edited.
    Also store who edited the message.
    """
    # Skip new messages
    if not instance.pk:
        return

    # Fetch old version from DB
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Check if content has changed
    if old_message.content != instance.content:

        # Create history record
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
            edited_by=instance.edited_by,   # save the editor
        )

        # Mark current message as edited
        instance.edited = True

