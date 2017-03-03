from rest_framework import permissions
from rest_framework.compat import is_authenticated

class AnyoneSignUpOrIsAuthenticated(permissions.BasePermission):
	def has_permission(self, request, view):
		if view.action == "create":
			return True
		elif request.user and is_authenticated(request.user):
			return True
		return False