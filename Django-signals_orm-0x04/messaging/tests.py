from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Message, Notification

User = get_user_model()


class MessageSignalTest(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(
            username="sender", password="1234"
        )
        self.receiver = User.objects.create_user(
            username="receiver", password="1234"
        )

    def test_notification_created_on_message(self):
        msg = Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

        # Check notification exists
        exists = Notification.objects.filter(message=msg, user=self.receiver).exists()
        self.assertTrue(exists)
