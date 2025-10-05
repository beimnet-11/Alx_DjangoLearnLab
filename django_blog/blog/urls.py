from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail-view'),
    path('post/new/', views.PostCreateView.as_view(), name='post-create-view'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update-view'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete-view'),
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment-create-view'),
    path('post/<int:pk>/comments/', views.CommentListView.as_view(), name='comments'),
    path('post/comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update-view'),
    path('post/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete-view'),
    path('tags/<slug:tag_slug>/', views.PostByTagListView.as_view(), name='posts-by-tag'),
    path('search/', views.SearchResultsView.as_view(), name='search'),
]
