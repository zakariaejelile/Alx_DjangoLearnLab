# blog/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm
from .models import Post
from django.contrib.auth.decorators import login_required

# Home View - Display all blog posts
def home(request):
    posts = Post.objects.all()  # Fetch all blog posts
    return render(request, 'blog/home.html', {'posts': posts})

# Register View - Handle user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile View - Handle profile edit
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to profile after saving
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

# Use Django's built-in LoginView (no need to create one from scratch)
class Login(LoginView):
    template_name = 'blog/login.html'  # Point to the login template

# Use Django's built-in LogoutView (no need to create one from scratch)
class Logout(LogoutView):
    next_page = '/'  # Redirect to homepage after logout

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post

# List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # your template
    context_object_name = 'posts'
    ordering = ['-published_date']  # latest posts first

# Show details of a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

# Create a new post (authenticated users only)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# Update a post (only author can update)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Delete a post (only author can delete)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/posts/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
