from rest_framework import permissions
from django.core import exceptions


class IsAuthor(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Read-only access for all requests: GET, OPTIONS, HEAD
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write access (create/update/delete) for the owner of the object
        if obj.author == request.user:
            return True

        raise exceptions.PermissionDenied(
            "You do not have permission to perform this action."
        )
