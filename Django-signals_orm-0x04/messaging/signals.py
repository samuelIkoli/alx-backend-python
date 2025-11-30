# messaging/signals.py

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

from .models import (
    Message,
    MessageHistory,
    Notification,
)

User = get_user_model()


# -----------------------------------------------------
# 1. EXISTING SIGNAL: create notification on new message
# -----------------------------------------------------
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Existing functionality:
    Creates a Notification whenever a new Message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# -----------------------------------------------------
# 2. NEW: pre_save history logger
# -----------------------------------------------------
@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    Saves a copy of old content into MessageHistory before a message is updated.
    """
    # Only run for updates, not new messages
    if not instance.pk:
        return

    try:
        old_msg = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # Only store history if content changed
    if old_msg.content != instance.content:
        MessageHistory.objects.create(
            message=old_msg,
            old_content=old_msg.content,
            edited_by=getattr(instance, "edited_by", None)
        )

        instance.edited = True
        instance.edited_at = timezone.now()


# -----------------------------------------------------
# 3. NEW REQUIREMENT: Cleanup related data on user deletion
# -----------------------------------------------------
@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    """
    Automatically cleans up:
    - sent messages
    - received messages
    - notifications
    - message edit histories
    when a user deletes their account.
    """

    # Delete messages the user sent
    sent_messages = Message.objects.filter(sender=instance)
    for msg in sent_messages:
        msg.delete()

    # Delete messages the user received
    received_messages = Message.objects.filter(receiver=instance)
    for msg in received_messages:
        msg.delete()

    # Delete notifications
    Notification.objects.filter(user=instance).delete()

    # Delete all MessageHistory records related to this user
    MessageHistory.objects.filter(edited_by=instance).delete()

    # If messages were linked via FK CASCADE,
    # their histories are already removed.
