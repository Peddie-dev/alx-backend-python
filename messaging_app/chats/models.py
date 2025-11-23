import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# -------------------------
# Custom User Model
# -------------------------
class User(AbstractUser):
    """
    Custom User model extending Django AbstractUser.

    Specifications:
    - user_id: UUID primary key
    - email: unique & required
    - role: ENUM('guest', 'host', 'admin')
    - phone_number: optional
    - password_hash: handled by Django's password field
    """

    ROLE_CHOICES = (
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    )

    user_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    # Django already includes:
    # - first_name
    # - last_name
    # - password  (hashed, meets password_hash requirement)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email}"


# -------------------------
# Conversation Model
# -------------------------
class Conversation(models.Model):
    """
    Conversations that include multiple users (many-to-many).

    Fields:
    - conversation_id: UUID primary key
    - participants: Many-to-many with User
    """

    conversation_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# -------------------------
# Message Model
# -------------------------
class Message(models.Model):
    """
    Messaging system

    Fields:
    - message_id: UUID primary key
    - sender: FK to User
    - conversation: FK to Conversation
    - message_body: text
    - sent_at: timestamp
    """

    message_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )

    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_sent"
    )

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )

    message_body = models.TextField(null=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.message_id} from {self.sender.email}"
from django.db import models

# Create your models here.
