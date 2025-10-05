from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from taggit.managers import TaggableManager

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Foreign key
    published_date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()
    
    def __str__(self):
        return f'{self.title}, {self.author}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.author}, {self.content}'
