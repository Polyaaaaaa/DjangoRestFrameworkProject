from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_staff
            or request.user.groups.filter(name="moderator").exists()
            or obj.owner == request.user
        )
