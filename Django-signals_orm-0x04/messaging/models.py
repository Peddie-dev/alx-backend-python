from django.db import models
from django.contrib.auth.models import User


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a specific user
        optimized for inbox display.
        """
        return (
            self.filter(receiver=user, read=False)
            .only("id", "sender", "content", "timestamp")
        )


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # ✅ NEW FIELD → unread / read tracking
    read = models.BooleanField(default=False)

    # Track if edited
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(
        User,
        related_name="edited_messages",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    # Threaded replies
    parent_message = models.ForeignKey(
        "self",
        related_name="replies",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # Managers
    objects = models.Manager()            # default
    unread = UnreadMessagesManager()      # custom

    def __str__(self):
        return f"Message {self.id} from {self.sender} to {self.receiver}"

    # ------------------------------------------------------------------
    #  RECURSIVE THREAD FETCHING
    # ------------------------------------------------------------------
    def get_thread(self):
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
        return (
            Message.objects.filter(
                parent_message__isnull=True,
                sender__in=[user1, user2],
                receiver__in=[user1, user2]
            )
            .select_related("sender", "receiver", "edited_by")
            .prefetch_related(
                "replies",
                "replies__sender",
                "replies__receiver",
                "replies__edited_by"
            )
            .order_by("timestamp")
        )


