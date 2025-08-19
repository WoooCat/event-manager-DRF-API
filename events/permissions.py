from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOrganizerOrReadOnly(BasePermission):
    """Read for all; write only for organizer of the event."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return getattr(obj, "organizer_id", None) == getattr(request.user, "id", None)
