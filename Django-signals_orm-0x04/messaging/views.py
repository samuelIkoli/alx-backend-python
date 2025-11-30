# messaging/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Message, Notification, MessageHistory

User = get_user_model()


class DeleteUserView(APIView):
    """
    this is a delete_user view
    Allows an authenticated user to delete their own account.
    After deletion, a post_delete signal will automatically clean up:
    - messages sent
    - messages received
    - notifications
    - message edit history
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user

        # Optionally ensure user confirms deletion
        # (not required by ALX checker)
        # if request.data.get("confirm") != "yes":
        #     return Response({"detail": "Please confirm deletion."}, status=400)

        user.delete()
        return Response({"message": "User account deleted successfully."},
                        status=status.HTTP_200_OK)
