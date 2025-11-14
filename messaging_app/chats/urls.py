from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # REQUIRED: must contain "api/"
    path('api/', include('chats.urls')),
]
