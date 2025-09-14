from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ('can_view', 'Can view'), ('can_delete', 'Can delete'), ('can_create', 'Can create'), ('can_edit', 'Can edit')
        ]

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        
        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    date_of_birth = models.DateTimeField(null=True, blank=True)
    profile_photo = models.ImageField()
    
    objects = CustomUserManager()