from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Notification


class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).order_by('-timestamp')

        data = []
        for notification in notifications:
            data.append({
                "id": notification.id,
                "actor": str(notification.actor),
                "verb": notification.verb,
                "is_read": notification.is_read,
                "timestamp": notification.timestamp,
            })

        return Response(data)
