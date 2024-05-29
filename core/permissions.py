from rest_framework.permissions import BasePermission


class Is_User(BasePermission):
    """
    Permission class to allow access only to the user who owns the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user is the owner of the object.

        Args:
            request (Request): The request object.
            view (View): The view object.
            obj (Object): The object being accessed.

        Returns:
            bool: True if the request user matches the object's user, False otherwise.
        """
        return request.user == obj


class AllowOnlyAuthorized(BasePermission):
    """
    Permission class to allow access only to authorized users.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authorized for the requested action.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user is authorized, False otherwise.
        """
        if request.method == "GET":
            return True
        elif request.user.is_authenticated and (
            request.user.role == "STAFF" or request.user.role == "ADMIN"
        ):
            return True
        return False


class IsAdmin(BasePermission):
    """
    Permission class to allow access only to users with the 'ADMIN' role.

    Attributes:
        message (str): Error message to display if permission is denied.
    """

    def has_permission(self, request, view):
        """
        Check if the user has the 'ADMIN' role.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has the 'ADMIN' role, False otherwise.
        """
        return bool(request.user and request.user.role == "ADMIN")


class AllowAny(BasePermission):
    """
    Permission class to allow access to any user.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the resource.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user has permission, False otherwise.
        """
        return True


class IsAuthenticated(BasePermission):
    """
    Permission class to allow access only to authenticated users.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated.

        Args:
            request (Request): The request object.
            view (View): The view object.

        Returns:
            bool: True if the user is authenticated, False otherwise.
        """
        return bool(request.user and request.user.is_authenticated)
