import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    
    # Role choices
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'
    
    # Custom fields - matching the specification exactly
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    first_name = models.CharField(max_length=150)  # VARCHAR, NOT NULL
    last_name = models.CharField(max_length=150)   # VARCHAR, NOT NULL
    email = models.EmailField(unique=True, db_index=True)  # VARCHAR, UNIQUE, NOT NULL
    phone_number = models.CharField(max_length=20, blank=True, null=True)  # VARCHAR, NULL
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST
    )
    created_at = models.DateTimeField(default=timezone.now)  # TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
    
    # Override the default username field to use email
    username = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """Model for tracking conversations between users"""
    
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    # According to spec: participants_id (Foreign Key, references User(user_id))
    # This means the conversation tracks which user is involved
    participant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations'
    )
    created_at = models.DateTimeField(default=timezone.now)  # TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Conversation with {self.participant}"


class Message(models.Model):
    """Model for storing messages in conversations"""
    
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message_body = models.TextField()  # TEXT, NOT NULL
    sent_at = models.DateTimeField(default=timezone.now)  # TIMESTAMP, DEFAULT CURRENT_TIMESTAMP
    
    class Meta:
        db_table = 'message'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['sender', 'sent_at']),
            models.Index(fields=['conversation', 'sent_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
