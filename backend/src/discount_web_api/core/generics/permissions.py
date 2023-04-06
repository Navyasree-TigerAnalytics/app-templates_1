from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    """Grants all permisisons for Admin role. Grants access to GET,HEAD,OPTIONS if role is ReadOnly.
    Grants access to PUT,PATCH,POST methods for ReadWrite role
    """

    edit_methods = ("PUT", "PATCH", "POST")

    def has_permission(self, request, view):

        if (
            request.user.role.role_name == "A"
            and request.user.is_authenticated
        ):
            return True

        if (
            request.user.is_authenticated
            and request.method in permissions.SAFE_METHODS
        ):
            return True

        if (
            request.user.is_authenticated
            and request.method in self.edit_methods
            and request.user.role.role_name != "R"
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.user.role.role_name == "A":
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if (
            request.method in self.edit_methods
            and request.user.role.role_name != "R"
        ):
            return True

        return False


class Group1Permissions(permissions.BasePermission):
    """Grants permission if the user belongs to Group1"""

    def has_permission(self, request, view):
        if request.user.group.group_id == 1:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.group.group_id == 1:
            return True
        return False


class Group2Permissions(permissions.BasePermission):
    """Grants permission if the user belongs to Group2"""

    def has_permission(self, request, view):
        if request.user.group.group_id == 2:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.group.group_id == 2:
            return True
        return False


class AdminOnly(permissions.BasePermission):
    """Grants permission if the user's role is Admin'"""

    def has_permission(self, request, view):
        if request.user.role.role_name == "A":
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role.role_name == "A":
            return True
        return False
