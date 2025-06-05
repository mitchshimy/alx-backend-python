from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access or modify messages.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):  # Conversation object
            return request.user in obj.participants.all()
        if hasattr(obj, 'conversation'):  # Message object
            return request.user in obj.conversation.participants.all()
        return False
