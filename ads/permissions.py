from rest_framework.permissions import BasePermission

from users.models import  UserRoles


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        elif hasattr(obj, 'author'):
            return obj.author == request.user
        else:
            raise AttributeError('Object has no attribute "owner" or "author"')


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in [UserRoles.ADMIN, UserRoles.MODERATOR]
