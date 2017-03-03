from rest_framework import permissions
from rest_framework.compat import is_authenticated

class AnyoneSignUpOrIsAuthenticated(permissions.BasePermission):
	def has_permission(self, request, view):
		"""
		Alow all to signup.
		Allow all logged in users to view other users.
		Allow owners to patch.
		"""
		if view.action == "create":
			return True
		elif view.action == "update" and \
			int(view.kwargs["pk"]) == request.user.id:
			return True
		elif view.action == "list" and \
			is_authenticated(request.user):
			return True
		return False