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

    # New field to track edits
    edited = models.BooleanField(default=False)

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"


class MessageHistory(models.Model):
    """
    Stores previous versions of a Message before it was edited.
    """
    message = models.ForeignKey(
        Message, related_name='history', on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for Message {self.message.id} at {self.edited_at}"

