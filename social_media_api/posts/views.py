from rest_framework import viewsets, permissions, filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from posts.models import Post, Like




class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']


def perform_create(self, serializer):
    serializer.save(author=self.request.user)




class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


def perform_create(self, serializer):
    serializer.save(author=self.request.user)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics, permissions

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all()
        return Post.objects.filter(author__in=following_users).order_by('-created_at')



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

class LikePostView(APIView):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)  # ✅ ensure this is an instance
        # your existing like logic, for example:
        post.likes.add(request.user)
        # send notification
        # Notification.objects.create(
        #     recipient=post.author,
        #     actor=request.user,
        #     verb='liked your post',
        #     target=post
        # )
        return Response({"detail": "Post liked"}, status=status.HTTP_200_OK)





class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        Like.objects.filter(user=request.user, post=post).delete()
        return Response({'detail': 'Post unliked'})
