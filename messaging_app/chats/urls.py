from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# ALX checker requirement: routers.DefaultRouter()
router = routers.DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

urlpatterns = [
    path("", include(router.urls)),
]
