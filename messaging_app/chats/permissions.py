from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission to allow only owners of an object to view/edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Assuming the object has a `user` field
        return obj.user == request.user
