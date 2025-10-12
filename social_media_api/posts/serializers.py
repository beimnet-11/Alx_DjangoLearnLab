from rest_framework import serializers
from django.contrib.auth import get_user_model
from . import models

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = models.Comment
        fields = ['id', 'post', 'content', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        return models.Comment.objects.create(author=request.user, **validated_data)

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    
    class Meta:
        model = models.Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        request = self.context.get('request')
        return models.Post.objects.create(author=request.user, **validated_data)

class LikeUnlikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = models.Like
        fields = ['post', 'user']