from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message, Notification, MessageHistory


# --------------------------------------------------
# 1️⃣ EXISTING REQUIREMENT — KEEP THIS
# Create Notification when a new Message is sent
# --------------------------------------------------
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    """
    Automatically create a notification for the receiver
    when a new message is created.
    """
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# --------------------------------------------------
# 2️⃣ NEW REQUIREMENT — ADD THIS
# Log old message content before it's edited
# --------------------------------------------------
@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    BEFORE saving a message, store old content in MessageHistory
    if the message content was changed.
    """

    # Only run on updates
    if not instance.pk:
        return

    try:
        old_msg = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content changed → log history
    if old_msg.content != instance.content:
        MessageHistory.objects.create(
            message=old_msg,
            old_content=old_msg.content,
            edited_by=getattr(instance, "edited_by", None)
        )

        # Mark main message as edited
        instance.edited = True
        instance.edited_at = timezone.now()
