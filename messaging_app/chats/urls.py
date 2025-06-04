from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Base router
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')  # Optional direct access

# Nested router: messages under conversations
conversations_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
]
