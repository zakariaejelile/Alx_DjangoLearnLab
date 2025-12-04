from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentUpdateView, CommentDeleteView,add_comment
)

urlpatterns = [
    # Homepage
    path('', views.home, name='blog-home'),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),

    # Blog post CRUD URLs
    path('posts/', PostListView.as_view(), name='post-list'),                  # List all posts
    path('post/new/', PostCreateView.as_view(), name='post-create'),          # Create a new post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),     # View post details
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),# Edit a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),# Delete a post

     # comment urls
    path("post/<int:pk>/comment/", add_comment, name="add_comment"),
    #path('post/<int:pk>/comments/new/', add_comment, name='comment-create'),             # create comment on post pk
    path('comment/<int:pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),   # edit comment by comment pk
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'), # delete comment by comment pk


]
