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


class IsSellerOrReadonly(BasePermission):
    """
    Custom permission to only allow sellers to edit their own products.
    """
    def has_permission(self, request, view):
        # Allow read-only access to all users
        if request.method in SAFE_METHODS:
            return True
        # Allow write access only to authenticated users who are sellers
        return request.user.role == 'seller' and request.user.is_authenticated
    

class IsProductOwner(BasePermission):
    """
    Custom permission to only allow the owner of a product to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access to all users
        if request.method in SAFE_METHODS:
            return True
        # Allow write access only to the owner of the product
        return obj.seller == request.user