from rest_framework import permissions
from .models import User

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superadmin()

class CanCreateAdminOrReviewer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_superadmin():
            return False
        role = request.data.get('role')
        return role in [User.Role.ORG_ADMIN, User.Role.REVIEWER] 