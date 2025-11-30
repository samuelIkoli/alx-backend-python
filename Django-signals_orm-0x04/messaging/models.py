# messaging/models.py

from django.db import models
from django.contrib.auth import get_user_model
from .managers import UnreadMessagesManager   # NEW import

User = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # NEW FIELD for unread manager
    read = models.BooleanField(default=False)

    # EDIT TRACKING (previous tasks)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="edited_messages"
    )

    # THREADED CONVERSATION (previous task)
    parent_message = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    # DEFAULT + CUSTOM MANAGERS
    objects = models.Manager()
    unread = UnreadMessagesManager()   # required by checker

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

    @classmethod
    def with_related(cls):
        return (
            cls.objects
            .select_related("sender", "receiver", "parent_message")
            .prefetch_related("replies")
        )

    def build_thread_tree(self):
        def build_node(msg):
            children = (
                msg.replies
                .all()
                .select_related("sender", "receiver", "parent_message")
            )
            return {
                "message": msg,
                "replies": [build_node(child) for child in children]
            }

        return build_node(self)


class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(
        Message, related_name="notifications", on_delete=models.CASCADE
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user} - Message ID {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User, null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="message_history_editor"
    )

    def __str__(self):
        return f"History for Message {self.message.id}"
