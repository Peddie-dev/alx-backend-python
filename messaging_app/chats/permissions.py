from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access and modify its messages.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission:
        - obj can be a Conversation or Message
        - Conversation model should have a ManyToMany field `participants`
        - Message model should have a ForeignKey `conversation`
        """
        if hasattr(obj, 'participants'):
            # Object is a Conversation
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            # Object is a Message
            return request.user in obj.conversation.participants.all()
        return False
