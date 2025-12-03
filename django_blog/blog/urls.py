"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'), 
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LoginView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),  # Profile page
]

"""

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views  # Make sure to import your views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]


from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),                 # List all posts
    path('posts/new/', PostCreateView.as_view(), name='post-create'),          # Create a new post
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),     # View post details
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),# Edit a post
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),# Delete a post
]



