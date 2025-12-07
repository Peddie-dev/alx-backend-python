from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # Track if the message has been edited
    edited = models.BooleanField(default=False)

    # NEW FIELD: who edited the message
    edited_by = models.ForeignKey(
        User,
        related_name='edited_messages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"


class MessageHistory(models.Model):
    """
    Stores previous versions of a Message before it is updated.
    """
    message = models.ForeignKey(
        Message, related_name='history', on_delete=models.CASCADE
    )
    old_content = models.TextField()

    # NEW FIELD: tracks who edited the message when this history record was created
    edited_by = models.ForeignKey(
        User,
        related_name='message_history_entries',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

