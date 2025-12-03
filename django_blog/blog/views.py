from django.shortcuts import render
from .models import Post

def home(request):
    posts = Post.objects.all() # Fetch all blog posts
    return render(request, 'blog/home.html', {'posts': posts})

from django.shortcuts import render,redirect
from .forms import CustomUserCreationForm

def register(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirect to login page after successful registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})


from django.contrib.auth.forms import UserChangeForm
from django.shortcuts import render, redirect

def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    
    return render(request, 'blog/profile.html', {'form': form})

