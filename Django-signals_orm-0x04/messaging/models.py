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

    # Track if edited
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name='edited_messages',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # NEW FIELD → enables threaded replies
    parent_message = models.ForeignKey(
        'self',
        related_name='replies',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    # ------------------------------------------------------------------
    #  RECURSIVE THREAD FETCHING
    # ------------------------------------------------------------------
    def get_thread(self):
        """
        Recursively fetch all replies to this message and return
        a tree-like structure as a nested list/dict.

        Format:
        {
            "message": <Message>,
            "replies": [...]
        }
        """
        return {
            "message": self,
            "replies": [
                reply.get_thread()
                for reply in self.replies.all().order_by("timestamp")
            ]
        }

    # ------------------------------------------------------------------
    #  HIGHLY OPTIMIZED QUERYING FOR UI & API
    # ------------------------------------------------------------------
    @staticmethod
    def fetch_conversation(user1, user2):
        """
        Returns all top-level messages between two users with optimal
        querying using select_related + prefetch_related.
        Replies are preloaded to avoid N+1 queries.
        """
        messages = (
            Message.objects.filter(
                parent_message__isnull=True,           # only top-level
                sender__in=[user1, user2],
                receiver__in=[user1, user2]
            )
            .select_related("sender", "receiver", "edited_by")
            .prefetch_related(
                "replies",                             # load replies
                "replies__sender",                     # load reply sender
                "replies__receiver",                   # load reply receiver
                "replies__edited_by"                   # load reply editor
            )
            .order_by("timestamp")
        )
        return messages


