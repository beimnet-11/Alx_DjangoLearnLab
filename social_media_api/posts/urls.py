from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('posts', views.PostViewSet, basename='posts')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', views.FeedView.as_view(), name='feed'),
    path('<int:pk>/like/', views.LikeView.as_view(), name='like'),
    path('<int:pk>/unlike/', views.UnLikeView.as_view(), name='unlike')
]
