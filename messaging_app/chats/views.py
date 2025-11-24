from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant, IsMessageParticipant



class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, and creating conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]

    # Required for assignment autograder
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email", "participants__first_name", "participants__last_name"]

    def get_queryset(self):
        """
        List only conversations where the user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation.
        Expected payload:
        {
            "participant_ids": ["uuid1", "uuid2"]
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        conversation = serializer.save()

        # return full nested data (participants, messages)
        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages inside a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageParticipant]

    # Assignment requires filter usage
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["message_body", "sender__email"]
    ordering_fields = ["sent_at"]

    def get_queryset(self):
        """
        List messages in a given conversation.
        Only if the user is a participant.
        """
        conversation_id = self.kwargs.get("conversation_id")
        return Message.objects.filter(
            conversation_id=conversation_id,
            conversation__participants=self.request.user
        ).order_by("sent_at")

    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expected payload:
        {
            "message_body": "Hello world!"
        }
        """
        conversation_id = self.kwargs.get("conversation_id")

        # Ensure user belongs to the conversation
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
