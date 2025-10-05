from django import forms
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Comment
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'content']
        widgets = {
            'tags': TagWidget()
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']