from rest_framework.permissions import BasePermission


class AllowOnlyAuthorized(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.user and (request.user.is_staff or request.user.is_superuser):
            return True
        return False