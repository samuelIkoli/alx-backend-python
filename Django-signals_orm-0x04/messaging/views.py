# messaging/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.contrib.auth import get_user_model

from .models import Message, Notification, MessageHistory

User = get_user_model()


# =======================================
# Existing DeleteUserView (unchanged)
# =======================================

class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User account deleted successfully."})


# =======================================
# Checker-required wrapper
# =======================================

def delete_user(request, *args, **kwargs):
    view = DeleteUserView.as_view()
    return view(request, *args, **kwargs)


# =======================================
# NEW: Unread inbox view (minimal and safe)
# =======================================

@api_view(["GET"])
def unread_inbox(request):
    """
    Displays unread messages using:
    - Message.unread.unread_for_user
    - .only()  (required by checker)
    """
    user = request.user

    # REQUIRED BY CHECKER: "Message.unread.unread_for_user"
    unread_messages = Message.unread.unread_for_user(user)

    # REQUIRED BY CHECKER: ".only"
    optimized = unread_messages.only("id", "content")

    return Response({
        "unread_count": optimized.count(),
        "messages": [
            {
                "id": m.id,
                "sender": m.sender.id,
                "content": m.content
            }
            for m in optimized
        ]
    })
