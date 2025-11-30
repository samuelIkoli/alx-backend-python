from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Message, MessageHistory


@receiver(pre_save, sender=Message)
def log_message_history(sender, instance, **kwargs):
    """
    BEFORE saving a message, keep a copy of the previous content.
    """

    # Only run on updates (existing messages)
    if not instance.pk:
        return

    try:
        old_instance = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    # If content changed → create history record
    if old_instance.content != instance.content:
        MessageHistory.objects.create(
            message=old_instance,
            old_content=old_instance.content,
            edited_by=getattr(instance, "edited_by", None)
        )

        # Update edited flag on main message
        instance.edited = True
        instance.edited_at = timezone.now()
