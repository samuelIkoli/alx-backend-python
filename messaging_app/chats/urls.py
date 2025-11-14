from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet
from django.contrib import admin

router = routers.DefaultRouter()
router.register("conversations", ConversationViewSet, basename="conversations")

urlpatterns = [
    path('admin/', admin.site.urls),

    # REQUIRED: must contain "api/"
    path('api/', include('chats.urls')),
]
