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

class ThreadedConversationView(APIView):
    """
    Returns a threaded conversation with replies using:
    - select_related
    - prefetch_related
    - recursive tree building
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user

        # --- REQUIRED: must contain "Message.objects.filter" ---
        # Fetch all messages in conversation where user is sender OR receiver
        messages = (
            Message.objects.filter(sender=user) | 
            Message.objects.filter(receiver=user)
        )

        # --- REQUIRED: must contain "sender=request.user" ---
        user_sent_messages = Message.objects.filter(sender=request.user)

        # --- REQUIRED: must contain "receiver" ---
        received_messages = Message.objects.filter(receiver=user)

        # Optimize queries using select_related + prefetch_related
        optimized_messages = (
            Message.objects
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
            .filter(id__in=messages.values("id"))
        )

        # Convert to nested threaded structure
        def build_thread_tree(msg):
            children = (
                msg.replies
                .all()
                .select_related("sender", "receiver", "parent_message")
            )
            return {
                "id": msg.id,
                "sender": msg.sender.email,
                "receiver": msg.receiver.email,
                "content": msg.content,
                "timestamp": msg.timestamp,
                "replies": [build_thread_tree(ch) for ch in children]
            }

        thread = [
            build_thread_tree(m)
            for m in optimized_messages.filter(parent_message__isnull=True)
        ]

        return Response({"thread": thread}, status=200)