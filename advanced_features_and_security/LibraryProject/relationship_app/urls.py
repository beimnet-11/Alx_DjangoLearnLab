from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import list_books, LibraryDetailView, home
from . import views

urlpatterns = [
    path('', list_books, name='list-books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
    path('register/', views.register, name='register'),
    path('home/', home, name='home'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.admin_view, name='librarian'),
    path('member/', views.admin_view, name='member'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/', views.change_book, name='change_book'),
    path('delete_book', views.delete_book, name='delete_book')
]