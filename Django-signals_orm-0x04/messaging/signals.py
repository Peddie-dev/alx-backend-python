from django.db.models.signals import post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Message, Notification, MessageHistory


@receiver(post_delete, sender=User)
def delete_related_user_data(sender, instance, **kwargs):
    """
    Cleans up user-related data when a User is deleted.
    This includes:
    - Messages sent or received
    - Notifications belonging to the user
    - MessageHistory entries created by the user
    """

    # DELETE messages where user is sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # DELETE notifications belonging to the user
    Notification.objects.filter(user=instance).delete()

    # DELETE histories where user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()

