from django.db import models
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
    
    # Custom fields
    user_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True
    )
    phone_number = models.CharField(
        max_length=20, 
        blank=True, 
        null=True
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.GUEST
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    # Override the default username field to use email
    username = None
    email = models.EmailField(
        unique=True,
        db_index=True
    )
    
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
    participants = models.ManyToManyField(
        User,
        related_name='conversations'
    )
    created_at = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        db_table = 'conversation'
        ordering = ['-created_at']
    
    def __str__(self):
        participant_names = [str(user) for user in self.participants.all()]
        return f"Conversation: {', '.join(participant_names)}"


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
    message_body = models.TextField()
    sent_at = models.DateTimeField(
        default=timezone.now
    )
    
    class Meta:
        db_table = 'message'
        ordering = ['sent_at']
        indexes = [
            models.Index(fields=['sender', 'sent_at']),
            models.Index(fields=['conversation', 'sent_at']),
        ]
    
    def __str__(self):
        return f"Message from {self.sender} at {self.sent_at}"
# Create your models here.
