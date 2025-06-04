# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow users to access their own messages/conversations only.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user  # assuming message has `user` field
