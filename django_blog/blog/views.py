from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views import generic
from django.urls import reverse_lazy
from . import models
from . import forms
from django.db.models import Q

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, 'blog/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = forms.CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = forms.CustomUserCreationForm()
    
    return render(request, 'blog/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def home_view(request):
    return render(request, 'blog/home.html')

@login_required
def profile_view(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        
        user = request.user
        user.username= new_username
        user.email = new_email
        user.save()
        
        return redirect('profile')
        
    else:
        return render(request, 'blog/profile.html')

class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/posts.html'
    context_object_name = 'posts'

class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = 'blog/posts_detail.html'
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin ,generic.CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'blog/post_create.html'
    login_url = 'login'
    success_url = reverse_lazy('posts')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(UserPassesTestMixin ,generic.UpdateView):
    model = models.Post
    template_name = 'blog/post_update.html'
    form_class = forms.PostForm
    login_url = 'login'
    success_url = reverse_lazy('posts')
    
    def test_func(self):
        post = self.get_object()
        return self.request.user ==  post.author

class PostDeleteView(generic.DeleteView):
    model = models.Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('posts')

class CommentListView(generic.ListView):
    model = models.Comment
    template_name = 'blog/comments.html'
    context_object_name = 'comments'
    
    def get_queryset(self):
        post_id = self.kwargs.get('pk')
        comments = models.Comment.objects.filter(id=post_id)
        return comments
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_id'] = self.kwargs.get('pk')  # pass post_id to template
        return context

class CommentCreateView(generic.CreateView):
    model = models.Comment
    form_class = forms.CommentForm
    template_name = 'blog/comment_create.html'    
    
    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')  # post id passed in URL
        post = get_object_or_404(models.Post, pk=post_pk)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'pk': self.kwargs.get('pk')})

class CommentUpdateView(generic.UpdateView):
    model = models.Comment
    form_class = forms.CommentForm
    template_name = 'blog/comment_update.html'
    
    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'pk': self.kwargs.get('pk')})

class CommentDeleteView(generic.DeleteView):
    model = models.Comment
    template_name = 'blog/comment_delete.html'
    
    def get_success_url(self):
        return reverse_lazy('comments', kwargs={'pk': self.kwargs.get('pk')})


class PostByTagListView(generic.ListView):
    model = models.Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_name = self.kwargs.get('tag_name')
        return models.Post.objects.filter(tags__name__iexact=tag_name).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_name'] = self.kwargs.get('tag_name')
        return context

class SearchResultsView(generic.ListView):
    model = models.Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return models.Post.objects.none()
        # search title, content, tags
        return models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()