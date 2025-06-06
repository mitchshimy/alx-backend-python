from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access or modify messages.
    Read-only access is allowed only for participants.
    Write access (PUT, PATCH, DELETE) is only allowed if the user is a participant.
    """

    def has_permission(self, request, view):
        # User must be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Determine if user is a participant in the object
        if hasattr(obj, 'participants'):  # Conversation object
            is_participant = request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):  # Message object
            is_participant = request.user in obj.conversation.participants.all()
        else:
            return False

        if request.method in SAFE_METHODS:
            # Allow read-only access if user is participant
            return is_participant
        else:
            # For PUT, PATCH, DELETE allow only if user is participant
            return is_participant

