from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only allows authenticated users
    - Only participants of a conversation can access messages or the conversation
    """

    def has_permission(self, request, view):
        # User must be authenticated to access the API
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission checks:
        obj can be Conversation or Message.
        """
        # If accessing a Conversation object
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()

        # If accessing a Message object
        if isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()

        return False


class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only to messages belonging to conversations
    the user participates in.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user in obj.conversation.participants.all()
