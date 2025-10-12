from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    
    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            Token.objects.filter(user=user).delete()
            token = Token.objects.create(user=user)
            return {"username": user.username, "token": token.key}
        raise ValidationError("Invalid Informations.")

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'bio', 'profile_picture', 'followers', 'following']

class FollowUnfollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['following']