import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Uses UUID as primary key and adds phone_number and role.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Remove username UNIQUE constraint, we will use email instead
    username = models.CharField(max_length=150, blank=True, null=True)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # removes username as required

    def __str__(self):
        return f"{self.email}"

class Conversation(models.Model):
    """
    Tracks a conversation involving multiple users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ManyToManyField('User', related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


class Message(models.Model):
    """
    Stores individual messages in a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    sender_id = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='messages_sent'
    )
    
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )

    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
