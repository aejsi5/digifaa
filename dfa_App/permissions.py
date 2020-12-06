from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    message= "You are only authorized to change objects you created"

    """
    Object-level permission to only see objects of the authenticated users client
    """

    def has_object_permission(self, request, view, obj):
        if obj.User == request.user:
            return True
        else:
            return False