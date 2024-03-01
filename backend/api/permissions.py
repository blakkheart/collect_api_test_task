from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    '''Доступ для создателя Группового сбора.'''

    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user == obj.author


class IsUser(permissions.BasePermission):
    '''Доступ для пользователя к своей истории.'''

    def has_permission(self, request, view):
        return view.kwargs.get('user_id') == request.user.id

    def has_object_permission(self, request, view, obj):
        return view.kwargs.get('user_id') == request.user.id
