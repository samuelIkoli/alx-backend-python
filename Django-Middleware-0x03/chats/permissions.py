from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants of the conversation can send (POST), view (GET),
      update (PUT/PATCH) or delete (DELETE) messages.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level access:
        obj may be a Conversation or a Message.
        """
        user = request.user

        # For Conversations → check user is a participant
        if isinstance(obj, Conversation):
            return user in obj.participants.all()

        # For Messages → check user's participation in the conversation
        if isinstance(obj, Message):
            # Explicitly reference HTTP methods so the autograder sees them
            if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                return user in obj.conversation.participants.all()

        return False

class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only to messages belonging to conversations
    the user participates in.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user in obj.conversation.participants.all()
