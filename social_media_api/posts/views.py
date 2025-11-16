from rest_framework import viewsets, filters, permissions, generics, status
from . import models
from . import serializers
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
from .models import Post, Like
from notifications.models import Notification
from rest_framework import generics
from django.contrib.contenttypes.models import ContentType

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class FeedView(generics.ListAPIView):
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return models.Post.objects.filter(author__in=following_users).order_by('-created_at')

class LikeView(generics.GenericAPIView):
    serializer_class = serializers.LikeUnlikeSerializer
    
    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if created:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb= f'{request.user.username} liked your video.',
                content_type = ContentType.objects.get_for_model(Post),
                object_id = post.id,
                target = post,
            )
            return Response({'liked': True}, status=status.HTTP_201_CREATED)
        else:
            # user already liked the post
            return Response({'liked': False, 'detail': 'Already liked'}, status=status.HTTP_200_OK)

class UnLikeView(generics.GenericAPIView):
    serializer_class = serializers.LikeUnlikeSerializer

    def post(self, request, pk):
        like = generics.get_object_or_404(Like, pk=pk)
        like.delete()

        return Response({"unlike": True}, status=status.HTTP_201_CREATED)