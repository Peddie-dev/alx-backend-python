from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allow only participants in a conversation to access messages.
    Works for all request methods including GET, POST, PUT, PATCH, DELETE.
    """

    def has_permission(self, request, view):
        # Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - Conversation: user must be a participant
        - Message: user must be a participant in the parent conversation
        """
        if hasattr(obj, 'participants'):
            # Conversation object
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Message object
            return request.user in obj.conversation.participants.all()
        return False
