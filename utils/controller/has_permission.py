from ninja_extra import permissions


class UserWithPermission(permissions.BasePermission):
    def __init__(self, permission: str) -> None:
        self._permission = permission

    def has_permission(self, request, view, controller=None):
        return request.user.has_perm(self._permission)
