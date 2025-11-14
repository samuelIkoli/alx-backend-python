from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    Handles listing, retrieving, and creating conversations.
    Uses a single serializer for both read & write.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer

    def get_queryset(self):
        """
        Only return conversations where the authenticated user is a participant.
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

        # Save conversation (participants already handled in serializer)
        conversation = serializer.save()

        # Return fully nested representation
        read_serializer = ConversationSerializer(conversation)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Handles listing messages and sending new messages in a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return messages that belong to a conversation the user participates in.
        """
        conversation_id = self.kwargs.get("conversation_id")

        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by("sent_at")

    def create(self, request, *args, **kwargs):
        """
        Send a message in an existing conversation.
        Expected JSON:
        {
            "message_body": "Hello world!"
        }
        """
        conversation_id = self.kwargs.get("conversation_id")

        # Check user is part of this conversation
        try:
            conversation = Conversation.objects.get(
                conversation_id=conversation_id,
                participants=request.user
            )
        except Conversation.DoesNotExist:
            return Response(
                {"error": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create the message
        message = Message.objects.create(
            sender=request.user,
            conversation=conversation,
            message_body=request.data.get("message_body")
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
