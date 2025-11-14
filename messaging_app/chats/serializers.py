from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()  # Required: SerializerMethodField()

    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'phone_number', 'role', 'created_at']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()
    message_body = serializers.CharField()  # Required: CharField

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender_id',
            'sender_name',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['sender']

    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"

    # Required: ValidationError
    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    # READ-ONLY nested relationships
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()

    # WRITE-ONLY participants input (for creating)
    participant_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        write_only=True,
        required=True
    )

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',      # nested (read)
            'participant_ids',   # raw IDs (write)
            'messages',          # nested
            'message_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_message_count(self, obj):
        return obj.messages.count()

    # VALIDATION
    def validate_participant_ids(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must include at least 2 participants."
            )
        return value

    # HANDLES CONVERSATION CREATION
    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        return conversation
