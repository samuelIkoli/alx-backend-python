from rest_framework import permissions
from .models import Conversation, Message


class IsConversationParticipant(permissions.BasePermission):
    """
    Allows access only to participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        return request.user in obj.participants.all()


class IsMessageParticipant(permissions.BasePermission):
    """
    Allows access only to messages belonging to conversations
    the user participates in.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user in obj.conversation.participants.all()
