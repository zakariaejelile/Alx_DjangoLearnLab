from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from django.contrib.auth import get_user_model, authenticate
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from .models import CustomUser


from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from notifications.models import Notification

User = get_user_model()

CustomUser.objects.all()


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
        )

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_400_BAD_REQUEST
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "user": UserSerializer(user).data,
            "token": token.key
        })


class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow == request.user:
            return Response(
                {"detail": "You cannot follow yourself"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user.following.add(user_to_follow)

        Notification.objects.create(
            recipient=user_to_follow,
            actor=request.user,
            verb="started following you",
            target=request.user
        )

        return Response({"detail": "User followed"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, id=user_id)
        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "User unfollowed"}, status=status.HTTP_200_OK)
