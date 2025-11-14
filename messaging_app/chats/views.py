from django.shortcuts import render

# Create your views here.


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles listing, retrieving, and creating conversations.
    Uses a single serializer for both read & write.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Only return conversations where the user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        
        Expected JSON:
        {
            "participant_ids": ["uuid1", "uuid2"]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create conversation instance
        conversation = serializer.save()

        # Return full nested response after creation
        read_serializer = ConversationSerializer(conversation)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing messages and sending new messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only allow listing messages that belong to a conversation
        the user is a participant in.
        """
        conversation_id = self.kwargs.get("conversation_id")
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_id")
        conversation = Conversation.objects.get(id=conversation_id)

        # Check user is part of the conversation
        if request.user not in conversation.participants.all():
            return Response(
                {"error": "You are not part of this conversation"},
                status=status.HTTP_403_FORBIDDEN
            )

        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=request.data.get("message_body")
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
