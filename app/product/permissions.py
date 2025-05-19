from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadonly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    """
    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in SAFE_METHODS:
            return True
        # Allow write access only to admin users
        return request.user and request.user.is_staff