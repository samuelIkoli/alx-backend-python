from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register("conversations", ConversationViewSet, basename="conversations")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "conversations/<uuid:conversation_id>/messages/",
        MessageViewSet.as_view({"get": "list", "post": "create"}),
        name="conversation-messages"
    ),
]
