from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from . import models
from . import serializers
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.exceptions import ValidationError

CustomUser = get_user_model()

# Create your views here.
class RegisterView(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer
    queryset = CustomUser.objects.all()
    


class LoginView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class ProfileView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.filter(id=user.id)

class FollowView(generics.GenericAPIView):
    serializer_class = serializers.FollowUnfollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        added_user = get_object_or_404(get_user_model(), id=user_id)

        if user.id == added_user.id:
            raise ValidationError('You cannot follow yourself.')
        
        user.following.add(added_user)

        serializer = self.get_serializer(user.following.all(), many=True)
        print(f'serializer: {serializer}')
        return Response(serializer.data, status=status.HTTP_200_OK)

class UnfollowView(generics.GenericAPIView):
    serializer_class = serializers.FollowUnfollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user = request.user
        get_unfollow_user = get_object_or_404(get_user_model(), id=user_id)

        if get_unfollow_user.id == user.id:
            raise ValidationError('You cannot unfollow yourself.')

        unfollow_user = get_object_or_404(user.following.all(), id=user_id)
        user.following.remove(unfollow_user)

        serializer = self.get_serializer(user.following.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)