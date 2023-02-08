from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsLibrarianOrUser(permissions.BasePermission):
    def can_edit(self, request):
        # if user is librarian, then library can be edited
        if request.user.is_staff:
            return True
